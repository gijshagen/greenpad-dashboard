from datetime import datetime

import pandas as pd
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models import Count
from django.db.models.functions import TruncDate

from .models import Trade


def upload_trades(request):
    """
    Uploadpagina voor IBKR / generieke trade-bestanden.

    Verwacht IBKR-achtige kolommen:

    - Symbol
    - Asset Category
    - Description
    - Currency
    - Trade Date      (YYYY-MM-DD)
    - Trade Time      (HH:MM:SS)
    - Quantity
    - T. Price
    - Comm/Fee
    - Buy/Sell        (BUY/SELL)
    """
    if request.method == "POST" and request.FILES.get("file"):
        upload = request.FILES["file"]
        filename = upload.name.lower()

        try:
            # 1) Lees bestand in met pandas
            if filename.endswith(".xlsx"):
                df = pd.read_excel(upload)
            elif filename.endswith(".csv"):
                # delimiter aanpassen als jouw export ; gebruikt
                df = pd.read_csv(upload)
            else:
                messages.error(request, "Alleen .csv en .xlsx bestanden worden ondersteund.")
                return redirect("trades:upload_trades")

            # 2) Verwachte kolommen controleren
            required_columns = [
                "Symbol",
                "Currency",
                "Trade Date",
                "Trade Time",
                "Quantity",
                "T. Price",
                "Comm/Fee",
                "Buy/Sell",
            ]

            missing = [col for col in required_columns if col not in df.columns]
            if missing:
                messages.error(
                    request,
                    f"Ontbrekende kolommen in upload: {', '.join(missing)}. "
                    f"Zorg dat je IBKR-export deze kolommen bevat."
                )
                return redirect("trades:upload_trades")

            trades_to_create = []

            for _, row in df.iterrows():
                # 3) Datum + tijd samenvoegen
                trade_date = row["Trade Date"]
                trade_time = row["Trade Time"]

                # trade_date/time kunnen als string of datetime binnenkomen → normaliseren
                if isinstance(trade_date, str):
                    date_str = trade_date
                else:
                    # pandas Timestamp → string YYYY-MM-DD
                    date_str = trade_date.strftime("%Y-%m-%d")

                if isinstance(trade_time, str):
                    time_str = trade_time
                else:
                    time_str = trade_time.strftime("%H:%M:%S")

                dt_str = f"{date_str} {time_str}"
                trade_datetime = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")

                # 4) Side normaliseren (BUY/SELL)
                side = str(row["Buy/Sell"]).strip().upper()

                # 5) Quantity, price, fee normaliseren
                quantity = row["Quantity"]
                price = row["T. Price"]
                fee = row["Comm/Fee"]

                # Soms geeft IBKR fee als negatief → we slaan absolute waarde op
                try:
                    fee = float(fee)
                    fee = abs(fee)
                except Exception:
                    fee = 0

                trades_to_create.append(
                    Trade(
                        broker="IBKR",  # default broker
                        symbol=str(row["Symbol"]).strip(),
                        isin=None,  # nog niet uit IBKR gelezen
                        trade_datetime=trade_datetime,
                        side=side,
                        quantity=quantity,
                        price=price,
                        fee=fee,
                        currency=str(row["Currency"]).strip(),
                    )
                )

            # 6) Opslaan in de database
            Trade.objects.bulk_create(trades_to_create)

            messages.success(request, f"{len(trades_to_create)} trades geïmporteerd.")
            return redirect("trades:upload_trades")

        except Exception as e:
            # In een echte app zou je dit loggen
            messages.error(request, f"Er ging iets mis bij het verwerken van het bestand: {e}")
            return redirect("trades:upload_trades")

    # GET-request: gewoon de pagina tonen
    return render(request, "trades/upload.html")


def dashboard(request):
    """
    Dashboard met een eerste grafiek:
    - aantal trades per dag
    """

    # trades groeperen per datum (op basis van trade_datetime)
    qs = (
        Trade.objects
        .annotate(day=TruncDate("trade_datetime"))
        .values("day")
        .annotate(trade_count=Count("id"))
        .order_by("day")
    )

    labels = [item["day"].strftime("%Y-%m-%d") for item in qs]
    data = [item["trade_count"] for item in qs]

    context = {
        "labels": labels,
        "data": data,
    }

    return render(request, "trades/dashboard.html", context)
