//+------------------------------------------------------------------+
//|                                            MT5_Local_Copier.mq5  |
//|                 Universal Copier - Full SL/TP & Pending Support  |
//+------------------------------------------------------------------+
#property copyright "Dedicated Copier"
#property version   "3.40"
#property strict

#include <Trade\Trade.mqh>

input int TimerMS = 150; 

CTrade trade;
string TerminalID;
string statusFileName;
string commandFileName;

int OnInit()
{
   TerminalID = "MT5_" + IntegerToString(AccountInfoInteger(ACCOUNT_LOGIN));
   statusFileName = "status_" + TerminalID + ".json";
   commandFileName = "cmd_" + TerminalID + ".json";
   
   trade.SetExpertMagicNumber(998877);
   trade.SetDeviationInPoints(50);

   Print("[Copier MT5 v3.40] فعال شد روی: ", TerminalID);
   
   WriteStatus();
   EventSetMillisecondTimer(TimerMS);
   return(INIT_SUCCEEDED);
}

void OnDeinit(const int reason)
{
   EventKillTimer();
}

void OnTick()
{
   WriteStatus();
   ProcessCommands();
}

void OnTimer()
{
   WriteStatus();
   ProcessCommands();
}

void WriteStatus()
{
   string json = "{\"terminal_id\":\"" + TerminalID + "\",\"platform\":\"MT5\",\"account\":" + IntegerToString(AccountInfoInteger(ACCOUNT_LOGIN)) + ",\"orders\":[";
   bool first = true;

   // ۱. پوزیشن‌های باز فعال
   int totalPositions = PositionsTotal();
   for(int i = 0; i < totalPositions; i++)
   {
      string pSymbol = PositionGetSymbol(i);
      ulong ticket = PositionGetInteger(POSITION_TICKET);
      if(ticket > 0)
      {
         if(!first) json += ",";
         
         long posType = PositionGetInteger(POSITION_TYPE);
         string typeStr = (posType == POSITION_TYPE_BUY) ? "BUY" : "SELL";

         json += "{\"ticket\":" + IntegerToString(ticket) + ",";
         json += "\"symbol\":\"" + pSymbol + "\",";
         json += "\"type\":\"" + typeStr + "\",";
         json += "\"volume\":" + DoubleToString(PositionGetDouble(POSITION_VOLUME), 2) + ",";
         json += "\"open_price\":" + DoubleToString(PositionGetDouble(POSITION_PRICE_OPEN), 5) + ",";
         json += "\"sl\":" + DoubleToString(PositionGetDouble(POSITION_SL), 5) + ",";
         json += "\"tp\":" + DoubleToString(PositionGetDouble(POSITION_TP), 5) + "}";
         first = false;
      }
   }

   // ۲. سفارش‌های پندینگ
   int totalOrders = OrdersTotal();
   for(int i = 0; i < totalOrders; i++)
   {
      ulong ordTicket = OrderGetTicket(i);
      if(ordTicket > 0)
      {
         long ordType = OrderGetInteger(ORDER_TYPE);
         string typeStr = "";
         if(ordType == ORDER_TYPE_BUY_LIMIT) typeStr = "BUY_LIMIT";
         else if(ordType == ORDER_TYPE_SELL_LIMIT) typeStr = "SELL_LIMIT";
         else if(ordType == ORDER_TYPE_BUY_STOP) typeStr = "BUY_STOP";
         else if(ordType == ORDER_TYPE_SELL_STOP) typeStr = "SELL_STOP";

         if(typeStr != "")
         {
            if(!first) json += ",";
            json += "{\"ticket\":" + IntegerToString(ordTicket) + ",";
            json += "\"symbol\":\"" + OrderGetString(ORDER_SYMBOL) + "\",";
            json += "\"type\":\"" + typeStr + "\",";
            json += "\"volume\":" + DoubleToString(OrderGetDouble(ORDER_VOLUME_INITIAL), 2) + ",";
            json += "\"open_price\":" + DoubleToString(OrderGetDouble(ORDER_PRICE_OPEN), 5) + ",";
            json += "\"sl\":" + DoubleToString(OrderGetDouble(ORDER_SL), 5) + ",";
            json += "\"tp\":" + DoubleToString(OrderGetDouble(ORDER_TP), 5) + "}";
            first = false;
         }
      }
   }

   json += "]}";

   int handle = FileOpen(statusFileName, FILE_WRITE | FILE_TXT | FILE_ANSI | FILE_COMMON | FILE_SHARE_READ | FILE_SHARE_WRITE);
   if(handle != INVALID_HANDLE)
   {
      FileWriteString(handle, json);
      FileClose(handle);
   }
}

string ExtractFieldString(string json, string key)
{
   string searchKey = "\"" + key + "\"";
   int pos = StringFind(json, searchKey);
   if(pos < 0) return "";
   int colon = StringFind(json, ":", pos + StringLen(searchKey));
   if(colon < 0) return "";
   int q1 = StringFind(json, "\"", colon + 1);
   if(q1 < 0) return "";
   int q2 = StringFind(json, "\"", q1 + 1);
   if(q2 < 0) return "";
   return StringSubstr(json, q1 + 1, q2 - q1 - 1);
}

double ExtractFieldNumber(string json, string key)
{
   string searchKey = "\"" + key + "\"";
   int pos = StringFind(json, searchKey);
   if(pos < 0) return 0.0;
   int colon = StringFind(json, ":", pos + StringLen(searchKey));
   if(colon < 0) return 0.0;
   int start = colon + 1;
   while(start < StringLen(json) && (StringGetCharacter(json, start) == ' ' || StringGetCharacter(json, start) == '\t'))
      start++;
   int end1 = StringFind(json, ",", start);
   int end2 = StringFind(json, "}", start);
   int end = -1;
   if(end1 >= 0 && end2 >= 0) end = MathMin(end1, end2);
   else if(end1 >= 0) end = end1;
   else end = end2;
   if(end < 0) return 0.0;
   return StringToDouble(StringSubstr(json, start, end - start));
}

long ExtractFieldLong(string json, string key)
{
   return (long)ExtractFieldNumber(json, key);
}

void ProcessCommands()
{
   if(!FileIsExist(commandFileName, FILE_COMMON)) return;

   int handle = FileOpen(commandFileName, FILE_READ | FILE_TXT | FILE_ANSI | FILE_COMMON | FILE_SHARE_READ | FILE_SHARE_WRITE);
   if(handle == INVALID_HANDLE) return;

   string content = "";
   while(!FileIsEnding(handle))
      content += FileReadString(handle);
   FileClose(handle);
   FileDelete(commandFileName, FILE_COMMON);

   StringTrimLeft(content);
   StringTrimRight(content);
   if(StringLen(content) < 5) return;

   int searchPos = 0;
   while(true)
   {
      int startObj = StringFind(content, "{", searchPos);
      if(startObj < 0) break;
      int endObj = StringFind(content, "}", startObj);
      if(endObj < 0) break;

      string objJson = StringSubstr(content, startObj, endObj - startObj + 1);
      searchPos = endObj + 1;

      string action = ExtractFieldString(objJson, "action");
      long masterTicket = ExtractFieldLong(objJson, "master_ticket");
      string symbol = ExtractFieldString(objJson, "symbol");
      string typeStr = ExtractFieldString(objJson, "type");
      double volume = ExtractFieldNumber(objJson, "volume");
      double price = ExtractFieldNumber(objJson, "price");
      double sl = ExtractFieldNumber(objJson, "sl");
      double tp = ExtractFieldNumber(objJson, "tp");

      if(action == "OPEN")
         ExecuteOpen(masterTicket, symbol, typeStr, volume, price, sl, tp);
      else if(action == "MODIFY")
         ExecuteModify(masterTicket, price, sl, tp);
      else if(action == "CLOSE")
         ExecuteClose(masterTicket);
   }
}

void SetBestFillingMode(string sym)
{
   uint filling = (uint)SymbolInfoInteger(sym, SYMBOL_FILLING_MODE);
   if((filling & SYMBOL_FILLING_FOK) != 0)
      trade.SetTypeFilling(ORDER_FILLING_FOK);
   else if((filling & SYMBOL_FILLING_IOC) != 0)
      trade.SetTypeFilling(ORDER_FILLING_IOC);
   else
      trade.SetTypeFilling(ORDER_FILLING_RETURN);
}

void ExecuteOpen(long masterTicket, string sym, string typeStr, double vol, double openPrice, double sl, double tp)
{
   string comment = IntegerToString(masterTicket);

   // چک وجود قبلی در پوزیشن‌ها
   for(int i = PositionsTotal() - 1; i >= 0; i--)
   {
      if(PositionGetSymbol(i) != "")
      {
         if(PositionGetString(POSITION_COMMENT) == comment)
            return;
      }
   }

   // چک وجود قبلی در اوردرهای پندینگ
   for(int i = OrdersTotal() - 1; i >= 0; i--)
   {
      ulong ot = OrderGetTicket(i);
      if(ot > 0 && OrderGetString(ORDER_COMMENT) == comment)
         return;
   }

   if(!TerminalInfoInteger(TERMINAL_TRADE_ALLOWED) || !MQLInfoInteger(MQL_TRADE_ALLOWED))
   {
      Print("[Copier MT5 ERROR] ترید خودکار غیرفعال است!");
      return;
   }

   if(!SymbolSelect(sym, true))
   {
      Print("[Copier MT5 Error] نماد یافت نشد: ", sym);
      return;
   }

   SetBestFillingMode(sym);

   double minLot = SymbolInfoDouble(sym, SYMBOL_VOLUME_MIN);
   double maxLot = SymbolInfoDouble(sym, SYMBOL_VOLUME_MAX);
   double stepLot = SymbolInfoDouble(sym, SYMBOL_VOLUME_STEP);
   if(stepLot > 0)
      vol = MathFloor(vol / stepLot) * stepLot;
   if(vol < minLot) vol = minLot;
   if(vol > maxLot) vol = maxLot;

   MqlTick tick;
   SymbolInfoTick(sym, tick);

   bool res = false;
   if(typeStr == "BUY")
   {
      double p = (tick.ask > 0) ? tick.ask : SymbolInfoDouble(sym, SYMBOL_ASK);
      res = trade.Buy(vol, sym, p, sl, tp, comment);
   }
   else if(typeStr == "SELL")
   {
      double p = (tick.bid > 0) ? tick.bid : SymbolInfoDouble(sym, SYMBOL_BID);
      res = trade.Sell(vol, sym, p, sl, tp, comment);
   }
   else if(typeStr == "BUY_LIMIT")
   {
      res = trade.BuyLimit(vol, openPrice, sym, sl, tp, ORDER_TIME_GTC, 0, comment);
   }
   else if(typeStr == "SELL_LIMIT")
   {
      res = trade.SellLimit(vol, openPrice, sym, sl, tp, ORDER_TIME_GTC, 0, comment);
   }
   else if(typeStr == "BUY_STOP")
   {
      res = trade.BuyStop(vol, openPrice, sym, sl, tp, ORDER_TIME_GTC, 0, comment);
   }
   else if(typeStr == "SELL_STOP")
   {
      res = trade.SellStop(vol, openPrice, sym, sl, tp, ORDER_TIME_GTC, 0, comment);
   }

   if(res)
      Print("[Copier MT5 SUCCESS] سفارش باز/ثبت شد: ", typeStr, " نماد: ", sym, " تیکت مستر: ", masterTicket);
   else
      Print("[Copier MT5 ERROR] خطا در ثبت ", typeStr, ": ", trade.ResultRetcode(), " - ", trade.ResultRetcodeDescription());
}

void ExecuteModify(long masterTicket, double price, double sl, double tp)
{
   string comment = IntegerToString(masterTicket);

   // ۱. اصلاح در پوزیشن‌های فعال
   for(int i = PositionsTotal() - 1; i >= 0; i--)
   {
      if(PositionGetSymbol(i) != "")
      {
         if(PositionGetString(POSITION_COMMENT) == comment)
         {
            ulong ticket = PositionGetInteger(POSITION_TICKET);
            bool res = trade.PositionModify(ticket, sl, tp);
            Print("[Copier MT5] اصلاح SL/TP پوزیشن: ", ticket, " (مستر: ", masterTicket, ") نتیجه: ", res);
            return;
         }
      }
   }

   // ۲. اصلاح در سفارش‌های پندینگ
   for(int i = OrdersTotal() - 1; i >= 0; i--)
   {
      ulong ticket = OrderGetTicket(i);
      if(ticket > 0)
      {
         if(OrderGetString(ORDER_COMMENT) == comment)
         {
            bool res = trade.OrderModify(ticket, price, sl, tp, ORDER_TIME_GTC, 0);
            Print("[Copier MT5] اصلاح سفارش پندینگ: ", ticket, " (مستر: ", masterTicket, ") نتیجه: ", res);
            return;
         }
      }
   }
}

void ExecuteClose(long masterTicket)
{
   string comment = IntegerToString(masterTicket);
   bool found = false;

   // ۱. بستن در پوزیشن‌ها
   for(int i = PositionsTotal() - 1; i >= 0; i--)
   {
      if(PositionGetSymbol(i) != "")
      {
         if(PositionGetString(POSITION_COMMENT) == comment)
         {
            ulong ticket = PositionGetInteger(POSITION_TICKET);
            Print("[Copier MT5] بستن پوزیشن فعال: ", ticket, " مستر: ", masterTicket);
            trade.PositionClose(ticket);
            found = true;
         }
      }
   }

   // ۲. حذف از سفارش‌های پندینگ (کنسل شدن)
   for(int i = OrdersTotal() - 1; i >= 0; i--)
   {
      ulong ticket = OrderGetTicket(i);
      if(ticket > 0)
      {
         if(OrderGetString(ORDER_COMMENT) == comment)
         {
            Print("[Copier MT5] حذف/کنسل اوردر پندینگ: ", ticket, " مستر: ", masterTicket);
            trade.OrderDelete(ticket);
            found = true;
         }
      }
   }

   if(!found)
      Print("[Copier MT5 Info] سفارشی با مستر تیکت ", masterTicket, " برای بستن یا حذف پیدا نشد.");
}
