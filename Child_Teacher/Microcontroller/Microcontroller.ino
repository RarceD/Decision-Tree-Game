
#include <WiFi.h>
#include <PubSubClient.h>
#include <FastLED.h>
#include "colors.h"

typedef enum
{
   INIT,
   WAITING,
   ON_GAME,
   CORRECT_ANSWER,
   INCORRECT_ANSWER,
   END_GAME,
   RANKING
} States;
#define BLINK_FRECUENCY 100 //in miliseconds
States state_machine = INIT;
CRGB leds[1];
WiFiClient wifiClient;
PubSubClient client(wifiClient);
typedef struct
{
   int len;
   char words[20];
} Search;
Search finds[5];
void setup_wifi()
{
   // We start by connecting to a WiFi network
   Serial.println();
   Serial.print("Connecting to ");
   Serial.println(ssid);

   WiFi.begin(ssid, password);
   while (WiFi.status() != WL_CONNECTED)
   {
      delay(500);
      Serial.print(".");
   }
   randomSeed(micros());
   Serial.println("");
   Serial.println("WiFi connected");
   Serial.println("IP address: ");
   Serial.println(WiFi.localIP());
}

void reconnect()
{
   // Loop until we're reconnected
   while (!client.connected())
   {
      Serial.print("Attempting MQTT connection...");
      // Create a random client ID
      String clientId = "TFG_B-";
      clientId += String(random(0xffff), HEX);
      // Attempt to connect
      if (client.connect(clientId.c_str(), MQTT_USER, MQTT_PASSWORD))
      {
         Serial.println("connected");

         client.subscribe(MQTT_TEXT);
         client.subscribe(MQTT_HOLA);
         client.subscribe(MQTT_ADIOS);
         client.subscribe(MQTT_LOVE);
         // client.subscribe(MQTT_TFG_START);
         // client.subscribe(MQTT_TFG_GAME);
         // client.subscribe(MQTT_TFG_END);
         client.subscribe(MQTT_CHILDREN_MOVE);
      }
      else
      {
         Serial.print("failed, rc=");
         Serial.print(client.state());
         Serial.println(" try again in 5 seconds");
         leds[0] = CRGB::OrangeRed;
         FastLED.show();
         // Wait 5 seconds before retrying
         uint32_t millix = millis();
         WiFi.begin(ssid, password);
         while (millis() - millix <= 10000 && WiFi.status() != WL_CONNECTED)
         {

            delay(500);
            Serial.print(".");
         }
         if (WiFi.status() == WL_CONNECTED)
            leds[0] = CRGB::BlanchedAlmond;
         else
            leds[0] = CRGB::Red;
         FastLED.show();
         delay(2000);
      }
   }
}
bool search_word(Search *finds, int len, char *payl)
{
   int i = 0; //payload index
   for (; i < len; i++)
   {
      // printf("%c \n", payload[i]);
      if (payl[i] == finds->words[0])
      {
         int l;
         bool match = false;
         for (l = 0; l < finds->len; l++)
            if (payl[i + l] == finds->words[l])
               match = true;
            else
            {
               match = false;
               break;
            }
         if (match)
            return true;
      }
   }
   return false;
}
void callback(char *topic, byte *payload, unsigned int length)
{
   Serial.println(topic);
   if (!strcmp(topic, MQTT_CHILDREN_MOVE))
   {
      //init -> waiting
      if (strstr((char *)(payload), "0xAA") != NULL)
      {
         state_machine = WAITING;
         Serial.println("init -> waiting");
      }
      //waiting -> on_game
      if (strstr((char *)(payload), "0xBB") != NULL)
      {
         state_machine = ON_GAME;
         Serial.println("waiting -> on_game");
      }
      //on_game -> correct
      if (strstr((char *)(payload), "0xCC") != NULL)
      {
         state_machine = CORRECT_ANSWER;
         Serial.println("on_game -> correct");
      }
      //on_game -> incorrect
      if (strstr((char *)(payload), "0xDD") != NULL)
      {
         state_machine = INCORRECT_ANSWER;
         Serial.println("on_game -> incorrect");
      }
      //on_game -> end_true
      if (strstr((char *)(payload), "0xEE") != NULL)
      {
         Serial.println("on_game -> end_true");
         leds[0] = CRGB::Blue;
         FastLED.show();
      }
      //on_game -> end_false
      if (strstr((char *)(payload), "0xFF") != NULL)
      {
         Serial.println("on_game -> end_false");
         leds[0] = CRGB::Red;
         FastLED.show();
      }
      //on_game -> ranking
      if (strstr((char *)(payload), "0xRR") != NULL)
      {
         Serial.println("on_game -> ranking");
         state_machine = RANKING;
         leds[0] = CRGB::Purple;
         FastLED.show();
      }
      if (strstr((char *)(payload), "RESET") != NULL)
      {
         Serial.println("RESET");
         state_machine = INIT;
         leds[0] = CRGB::White;
         FastLED.show();
      }
   }

   if (!strcmp(topic, MQTT_TEXT))
   {
      bool sol = false;
      if (strstr((char *)(payload), word_1) != NULL || strstr((char *)(payload), word_2) != NULL)
         sol = true;
      if (strstr((char *)(payload), word_3) != NULL || strstr((char *)(payload), word_4) != NULL)
         sol = true;
      if (strstr((char *)(payload), word_5) != NULL || strstr((char *)(payload), word_6) != NULL)
         sol = true;
      if (strstr((char *)(payload), word_7) != NULL || strstr((char *)(payload), word_8) != NULL)
         sol = true;
      if (strstr((char *)(payload), word_9) != NULL || strstr((char *)(payload), word_10) != NULL)
         sol = true;

      if (sol)
         leds[0] = CRGB::LawnGreen;
      else
         leds[0] = CRGB::DarkViolet;
      FastLED.show();
      delay(100);
   }
   else if (!strcmp(topic, MQTT_TFG_START))
   {
      leds[0] = CRGB::Blue;
      FastLED.show();
   }
   else if (!strcmp(topic, MQTT_TFG_GAME))
   {
      leds[0] = CRGB::Purple;
      FastLED.show();
   }
   else if (!strcmp(topic, MQTT_TFG_END))
   {
      leds[0] = CRGB::SeaGreen;
      FastLED.show();
   }
   else if (!strcmp(topic, MQTT_HOLA))
   {
      leds[0] = CRGB::SkyBlue;
      FastLED.show();
   }
   else if (!strcmp(topic, MQTT_ADIOS))
   {
      leds[0] = CRGB::Green;
      FastLED.show();
   }
   else if (!strcmp(topic, MQTT_LOVE))
   {
      leds[0] = CRGB::OliveDrab;
      FastLED.show();
   }
}

void setup()
{
   Serial.begin(115200);
   FastLED.addLeds<NEOPIXEL, 2>(leds, 1);
   leds[0] = CRGB::OrangeRed;
   FastLED.show();
   delay(1000);
   Serial.setTimeout(500); // Set time out for
   setup_wifi();
   client.setServer(mqtt_server, mqtt_port);
   client.setCallback(callback);
   reconnect();
   uint64_t millix = millis();
   bool blink_status = true;
   //I first initialize the led to white:
   leds[0] = CRGB::White;
   FastLED.show();

   while (true)
   {
      switch (state_machine)
      {
      case INIT:
         millix = millis();
         break;
      case WAITING:
         if (millis() - millix >= BLINK_FRECUENCY)
         {
            Serial.println("blink the waitting led");
            if (blink_status)
            {
               blink_status = false;
               leds[0] = CRGB::Black;
            }
            else
            {
               leds[0] = CRGB::Yellow;
               blink_status = true;
            }
            FastLED.show();
            millix = millis();
         }
         break;
      case ON_GAME:
         break;
      case CORRECT_ANSWER:
         for (int i = 0; i < 4; i++)
         {
            Serial.println("blink the correct led");
            leds[0] = CRGB::Green;
            FastLED.show();
            delay(BLINK_FRECUENCY);
            leds[0] = CRGB::White;
            FastLED.show();
            delay(BLINK_FRECUENCY);
         }
         state_machine = ON_GAME;
         break;
      case INCORRECT_ANSWER:
         for (int i = 0; i < 4; i++)
         {
            Serial.println("blink the wrong led");
            leds[0] = CRGB::Red;
            FastLED.show();
            delay(BLINK_FRECUENCY);
            leds[0] = CRGB::White;
            FastLED.show();
            delay(BLINK_FRECUENCY);
         }
         state_machine = ON_GAME;
         break;
      case END_GAME:
         break;
      case RANKING:
         break;
      default:
         break;
      }
      reconnect();
      client.loop();
   }
}

void loop()
{
}
