//+------------------------------------------------------------------+
//|                                                        Saver.mq4 |
//|                                  Copyright 2023, MetaQuotes Ltd. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2023, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property strict
//--- input parameters
input string   host="https://localhost/account/"; //Api host
input string   account_number="00000000"; //Account number

enum ENUM_ACCOUNT
{
    CentDemo,
    AdvantageDemo,
    AdvantagePlusDemo,
    CentReal,
    AdvantageReal,
    AdvantagePlusReal,
    OtherDemo,
    OtherReal  
};


input ENUM_ACCOUNT enum_type_of_account=CentDemo; //Type of account


   string accountTypeStrings[OtherReal+1] =
   {
      "CentDemo",
      "AdvantageDemo",
      "AdvantagePlusDemo",
      "Cent Real",
      "AdvantageReal",
      "AdvantagePlusReal",
      "Other Demo",
      "Other Real"
   };

string str_type_of_account =accountTypeStrings[enum_type_of_account] +"("+ AccountCurrency()+")";

input int bar_size=1;// bar size in minutes
input int report_hour=16;//report hour
input int GMT_offset=6;

double equity[4];
double balance[4];
bool sent =False;
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
//---

   PostCreateAccount();
   EventSetTimer(60*bar_size);
   setbar();

//---
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//---
   EventKillTimer();
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
//---
   actualizebar();
   
  }
//+------------------------------------------------------------------+
void OnTimer()
   {
   if (IsMarketOpen())
   {
   closebar();
   PostBar(equity[0],equity[1],equity[2],equity[3],balance[0],balance[1],balance[2],balance[3]);
   setbar();
   
   if(report_hour==(TimeHour(TimeGMT()-(GMT_offset*3600))))
   {
   if(sent==False)
     {
      
      PostReport();
      
      sent=True;
     }
   }
   else{
   sent=False;
   }
   
   }
   
   }

bool IsMarketOpen()
{
    double tradeAllowed = MarketInfo(Symbol(), MODE_TRADEALLOWED);
    return (tradeAllowed == 1);
}

void PostCreateAccount()
{

         string JSON_string = StringConcatenate( "{",                                                    // **** MQL4 can concat max 63 items
                                              "\"account_id\"",
                                              ":",
                                              "\"",
                                              account_number,
                                              "\"",
                                              ",",
                                              "\"initial_amount\"",
                                              ":",
                                              AccountBalance(),
                                              ",",
                                              "\"type_of_account\"",
                                              ":",
                                              "\"",
                                              str_type_of_account,
                                              "\"",
                                              "}"
                                              );
                                              
         string  ReqSERVER_URL = "http://localhost/account/",              // ---- MQL4 WebRequst
                  ReqCOOKIE     =  NULL,
               // ReqHEADERs    =               "application/json"; // **** MQL4 WebRequest MUST   use [in]  Request headers of type "key: value", separated by a line break "\r\n".
                  ReqHEADERs    = "Content-Type: application/json\r\n";
          int     ReqTIMEOUT    =  5000;                            // ---- MQL4 WebRequest SHALL  use [in]  Timeouts below 1000 (1 sec.) are not enough for slow Internet connection;
               // ================================================= // ~~~~ MQL4 WebRequest SHALL be AVOIDED as an un-control-able BLOCKING-SHOW-STOPPER, any professional need shall use NON-BLOCKING tools
          char    POSTed_DATA[],
                  result_RECVed_DATA_FromSERVER[];
          int     result_RetCODE;
          string  result_DecodedFromSERVER,
                  result_RECVed_HDRs_FromSERVER;

       // int     intHostNameLength                       = StringLen(  ReqSERVER_URL );
       // StringToCharArray( ReqSERVER_URL, POSTed_DATA, 0, StringLen(  ReqSERVER_URL ) );
       // StringToCharArray( prmParameter,  post,        0, intHostNameLength );
          StringToCharArray( JSON_string,   POSTed_DATA, 0, StringLen(  JSON_string   ) );

          ResetLastError();

          result_RetCODE = WebRequest( "POST",
                                       ReqSERVER_URL,
                                       ReqHEADERs,
                                       ReqTIMEOUT,
                                       POSTed_DATA,
                                       result_RECVed_DATA_FromSERVER,
                                       result_RECVed_HDRs_FromSERVER
                                       );
                                       
          Print(result_RetCODE);
          if (  result_RetCODE == -1 ) Print( "Error in WebRequest. Error code  =", GetLastError() ); // returns error 4060 – "Function is not allowed for call" unless permitted -- ref. Picture in >>> https://stackoverflow.com/questions/39954177/how-to-send-a-post-with-a-json-in-a-webrequest-call-using-mql4
          else {
                for (  int i = 0; i < ArraySize( result_RECVed_DATA_FromSERVER ); i++ ) {
                       if (  ( result_RECVed_DATA_FromSERVER[i] == 10 ) // == '\n'  // <LF>
                          || ( result_RECVed_DATA_FromSERVER[i] == 13 ) // == '\r'  // <CR>
                          ) 
                          continue;
                       else     result_DecodedFromSERVER += CharToStr( result_RECVed_DATA_FromSERVER[i] );
                }
                Print( "DATA:: ", result_DecodedFromSERVER );
                Print( "HDRs:: ", result_RECVed_HDRs_FromSERVER );
          }
}




void PostBar(double equity_open,
             double equity_high,
             double equity_low,
             double equity_close,
             double balance_open,
             double balance_high,
             double balance_low,
             double balance_close)
{

         string JSON_string = StringConcatenate( "{",                                                    // **** MQL4 can concat max 63 items
                                              "\"account_id\"",
                                              ":",
                                              "\"",
                                              account_number,
                                              "\"",
                                              ",",
                                              "\"date_time\"",
                                              ":",
                                              "\"",
                                              TimeToString( TimeLocal(), TIME_DATE | TIME_SECONDS ),
                                              "\"",
                                              ",",
                                              "\"equity_open\"",
                                              ":",
                                              DoubleToString(equity_open,4),
                                              ",",
                                              "\"equity_high\"",
                                              ":",
                                              DoubleToString(equity_high,4),
                                              ",",
                                              "\"equity_low\"",
                                              ":",
                                              DoubleToString(equity_low, 4 ),
                                              ",",
                                              "\"equity_close\"",
                                              ":",
                                              DoubleToString(equity_close, 4 ),
                                              ",",
                                              "\"balance_open\"",
                                              ":",
                                              DoubleToString(balance_open, 4 ),
                                              ",",
                                              "\"balance_high\"",
                                              ":",
                                              DoubleToString(balance_high, 4 ),
                                              ",",
                                              "\"balance_low\"",
                                              ":",
                                              DoubleToString(balance_low, 4 ),
                                              ",",
                                              "\"balance_close\"",
                                              ":",
                                              DoubleToString(balance_close, 4 ),
                                              "}"
                                              );
                                              
         string  ReqSERVER_URL = "http://localhost/account/addbar",              // ---- MQL4 WebRequst
                  ReqCOOKIE     =  NULL,
               // ReqHEADERs    =               "application/json"; // **** MQL4 WebRequest MUST   use [in]  Request headers of type "key: value", separated by a line break "\r\n".
                  ReqHEADERs    = "Content-Type: application/json\r\n";
          int     ReqTIMEOUT    =  5000;                            // ---- MQL4 WebRequest SHALL  use [in]  Timeouts below 1000 (1 sec.) are not enough for slow Internet connection;
               // ================================================= // ~~~~ MQL4 WebRequest SHALL be AVOIDED as an un-control-able BLOCKING-SHOW-STOPPER, any professional need shall use NON-BLOCKING tools
          char    POSTed_DATA[],
                  result_RECVed_DATA_FromSERVER[];
          int     result_RetCODE;
          string  result_DecodedFromSERVER,
                  result_RECVed_HDRs_FromSERVER;

       // int     intHostNameLength                       = StringLen(  ReqSERVER_URL );
       // StringToCharArray( ReqSERVER_URL, POSTed_DATA, 0, StringLen(  ReqSERVER_URL ) );
       // StringToCharArray( prmParameter,  post,        0, intHostNameLength );
          StringToCharArray( JSON_string,   POSTed_DATA, 0, StringLen(  JSON_string   ) );

          ResetLastError();

          result_RetCODE = WebRequest( "POST",
                                       ReqSERVER_URL,
                                       ReqHEADERs,
                                       ReqTIMEOUT,
                                       POSTed_DATA,
                                       result_RECVed_DATA_FromSERVER,
                                       result_RECVed_HDRs_FromSERVER
                                       );
                                       
          Print(result_RetCODE);
          if (  result_RetCODE == -1 ) Print( "Error in WebRequest. Error code  =", GetLastError() ); // returns error 4060 – "Function is not allowed for call" unless permitted -- ref. Picture in >>> https://stackoverflow.com/questions/39954177/how-to-send-a-post-with-a-json-in-a-webrequest-call-using-mql4
          else {
                for (  int i = 0; i < ArraySize( result_RECVed_DATA_FromSERVER ); i++ ) {
                       if (  ( result_RECVed_DATA_FromSERVER[i] == 10 ) // == '\n'  // <LF>
                          || ( result_RECVed_DATA_FromSERVER[i] == 13 ) // == '\r'  // <CR>
                          ) 
                          continue;
                       else     result_DecodedFromSERVER += CharToStr( result_RECVed_DATA_FromSERVER[i] );
                }
                Print( "DATA:: ", result_DecodedFromSERVER );
                Print( "HDRs:: ", result_RECVed_HDRs_FromSERVER );
          }
      }

void PostReport()
{

         string JSON_string = StringConcatenate( "{",                                                    // **** MQL4 can concat max 63 items
                                              "\"account_id\"",
                                              ":",
                                              "\"",
                                              account_number,
                                              "\"",
                                              "}"
                                              );
                                              
         string  ReqSERVER_URL = "http://localhost/account/report",              // ---- MQL4 WebRequst
                  ReqCOOKIE     =  NULL,
               // ReqHEADERs    =               "application/json"; // **** MQL4 WebRequest MUST   use [in]  Request headers of type "key: value", separated by a line break "\r\n".
                  ReqHEADERs    = "Content-Type: application/json\r\n";
          int     ReqTIMEOUT    =  5000;                            // ---- MQL4 WebRequest SHALL  use [in]  Timeouts below 1000 (1 sec.) are not enough for slow Internet connection;
               // ================================================= // ~~~~ MQL4 WebRequest SHALL be AVOIDED as an un-control-able BLOCKING-SHOW-STOPPER, any professional need shall use NON-BLOCKING tools
          char    POSTed_DATA[],
                  result_RECVed_DATA_FromSERVER[];
          int     result_RetCODE;
          string  result_DecodedFromSERVER,
                  result_RECVed_HDRs_FromSERVER;

       // int     intHostNameLength                       = StringLen(  ReqSERVER_URL );
       // StringToCharArray( ReqSERVER_URL, POSTed_DATA, 0, StringLen(  ReqSERVER_URL ) );
       // StringToCharArray( prmParameter,  post,        0, intHostNameLength );
          StringToCharArray( JSON_string,   POSTed_DATA, 0, StringLen(  JSON_string   ) );

          ResetLastError();

          result_RetCODE = WebRequest( "POST",
                                       ReqSERVER_URL,
                                       ReqHEADERs,
                                       ReqTIMEOUT,
                                       POSTed_DATA,
                                       result_RECVed_DATA_FromSERVER,
                                       result_RECVed_HDRs_FromSERVER
                                       );
                                       
          Print(result_RetCODE);
          if (  result_RetCODE == -1 ) Print( "Error in WebRequest. Error code  =", GetLastError() ); // returns error 4060 – "Function is not allowed for call" unless permitted -- ref. Picture in >>> https://stackoverflow.com/questions/39954177/how-to-send-a-post-with-a-json-in-a-webrequest-call-using-mql4
          else {
                for (  int i = 0; i < ArraySize( result_RECVed_DATA_FromSERVER ); i++ ) {
                       if (  ( result_RECVed_DATA_FromSERVER[i] == 10 ) // == '\n'  // <LF>
                          || ( result_RECVed_DATA_FromSERVER[i] == 13 ) // == '\r'  // <CR>
                          ) 
                          continue;
                       else     result_DecodedFromSERVER += CharToStr( result_RECVed_DATA_FromSERVER[i] );
                }
                Print( "DATA:: ", result_DecodedFromSERVER );
                Print( "HDRs:: ", result_RECVed_HDRs_FromSERVER );
          }
}




void setbar(){

   equity[0]=AccountEquity();
   equity[1]=AccountEquity();
   equity[2]=AccountEquity();
   equity[3]=AccountEquity();
    
   balance[0]=AccountBalance(); 
   balance[1]=AccountBalance();   
   balance[2]=AccountBalance();  
   balance[3]=AccountBalance();  
}

void actualizebar(){
   if (AccountEquity()>equity[1]){
   equity[1]=AccountEquity();
   }
   if (AccountEquity()<equity[2]){
   equity[2]=AccountEquity();
   }
   
   if (AccountBalance()>balance[1]){
   balance[1]=AccountBalance();
   }
   if (AccountBalance()<balance[2]){
   balance[2]=AccountBalance();
   }  
}

void closebar(){
   equity[3]=AccountEquity();
   balance[3]=AccountBalance();
}