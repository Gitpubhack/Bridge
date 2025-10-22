"""
Background tasks for Bridge Exchange
"""
import asyncio
from datetime import datetime, timedelta
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from database import AsyncSessionLocal
from models.invoice import Invoice, InvoiceStatus
from models.transaction import Transaction, TransactionStatus
from models.stake import Stake
from services.cryptopay import CryptoPayClient
from services.bybit import BybitClient
from services.gecko import GeckoClient
from config import INVOICE_POLLING_INTERVAL, PRICE_UPDATE_INTERVAL, RECONCILE_INTERVAL

cryptopay = CryptoPayClient()
bybit = BybitClient()
gecko = GeckoClient()

async def poll_invoices():
    """Poll pending invoices and update status"""
    async with AsyncSessionLocal() as db:
        try:
            # Get pending invoices
            result = await db.execute(
                select(Invoice).where(Invoice.status == InvoiceStatus.PENDING)
            )
            invoices = result.scalars().all()
            
            for invoice in invoices:
                try:
                    # Check invoice status with CryptoPay
                    invoice_data = await cryptopay.get_invoice(invoice.provider_invoice_id)
                    
                    if invoice_data.get("ok") and invoice_data["result"]["status"] == "paid":
                        # Update invoice status
                        invoice.status = InvoiceStatus.PAID
                        await db.commit()
                        
                        # Credit user balance
                        from backend.routers.wallet import update_balance
                        await update_balance(db, invoice.user_id, invoice.asset, invoice.amount)
                        
                        # Create transaction record
                        transaction = Transaction(
                            user_id=invoice.user_id,
                            type=TransactionType.DEPOSIT,
                            amount=invoice.amount,
                            asset=invoice.asset,
                            status=TransactionStatus.COMPLETED,
                            meta={"invoice_id": invoice.id}
                        )
                        db.add(transaction)
                        await db.commit()
                        
                except Exception as e:
                    print(f"Error processing invoice {invoice.id}: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error in poll_invoices: {e}")

async def update_prices():
    """Update cryptocurrency prices"""
    try:
        # Get prices from CoinGecko
        prices = await gecko.get_price(
            ids=["bitcoin", "ethereum", "tether", "binancecoin", "cardano"],
            vs_currencies=["usd"]
        )
        
        # Store prices in cache or database
        # This is a simplified version - in production, you'd store in Redis or database
        print(f"Updated prices: {prices}")
        
    except Exception as e:
        print(f"Error updating prices: {e}")

async def calculate_staking_rewards():
    """Calculate and distribute staking rewards"""
    async with AsyncSessionLocal() as db:
        try:
            # Get active stakes
            result = await db.execute(
                select(Stake).where(Stake.is_active == True)
            )
            stakes = result.scalars().all()
            
            for stake in stakes:
                # Calculate rewards
                days_staked = (datetime.utcnow() - stake.since).days
                total_rewards = stake.amount * stake.apr / Decimal("365") * days_staked
                unclaimed_rewards = total_rewards - stake.rewards_claimed
                
                if unclaimed_rewards > 0:
                    # Update stake with new rewards
                    stake.rewards_claimed = total_rewards
                    await db.commit()
                    
                    # Credit rewards to user balance
                    from backend.routers.wallet import update_balance
                    await update_balance(db, stake.user_id, stake.asset, unclaimed_rewards)
                    
        except Exception as e:
            print(f"Error calculating staking rewards: {e}")

async def reconcile_transactions():
    """Reconcile pending transactions"""
    async with AsyncSessionLocal() as db:
        try:
            # Get pending withdrawals
            result = await db.execute(
                select(Transaction).where(
                    and_(
                        Transaction.type == TransactionType.WITHDRAW,
                        Transaction.status == TransactionStatus.PENDING
                    )
                )
            )
            withdrawals = result.scalars().all()
            
            for withdrawal in withdrawals:
                try:
                    # Check if withdrawal was processed externally
                    # This is a simplified version - in production, you'd check blockchain
                    
                    # For now, just mark as completed after some time
                    if datetime.utcnow() - withdrawal.created_at > timedelta(hours=1):
                        withdrawal.status = TransactionStatus.COMPLETED
                        await db.commit()
                        
                except Exception as e:
                    print(f"Error reconciling withdrawal {withdrawal.id}: {e}")
                    
        except Exception as e:
            print(f"Error in reconcile_transactions: {e}")

async def monitor_external_apis():
    """Monitor external API health"""
    try:
        # Check CryptoPay
        try:
            await cryptopay.get_me()
            print("CryptoPay API: OK")
        except Exception as e:
            print(f"CryptoPay API: ERROR - {e}")
        
        # Check Bybit
        try:
            await bybit.get_server_time()
            print("Bybit API: OK")
        except Exception as e:
            print(f"Bybit API: ERROR - {e}")
        
        # Check CoinGecko
        try:
            await gecko.get_price(["bitcoin"], ["usd"])
            print("CoinGecko API: OK")
        except Exception as e:
            print(f"CoinGecko API: ERROR - {e}")
            
    except Exception as e:
        print(f"Error monitoring APIs: {e}")

async def run_background_tasks():
    """Run all background tasks"""
    while True:
        try:
            # Run tasks in parallel
            await asyncio.gather(
                poll_invoices(),
                update_prices(),
                calculate_staking_rewards(),
                reconcile_transactions(),
                monitor_external_apis(),
                return_exceptions=True
            )
            
            # Wait before next iteration
            await asyncio.sleep(60)  # Run every minute
            
        except Exception as e:
            print(f"Error in background tasks: {e}")
            await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(run_background_tasks())
