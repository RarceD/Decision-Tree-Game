
#include <WiFi.h>
#include <PubSubClient.h>
#include <FastLED.h>
#include "colors.h"

CRGB leds[1];
WiFiClient wifiClient;
PubSubClient client(wifiClient);

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
         client.subscribe(MQTT_TFG_START);
         client.subscribe(MQTT_TFG_GAME);
         client.subscribe(MQTT_TFG_END);
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

void callback(char *topic, byte *payload, unsigned int length)
{
   Serial.println(topic);

   if (!strcmp(topic, MQTT_TEXT))
   {
      leds[0] = CRGB::Red;
      FastLED.show();
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
   leds[0] = CRGB::BlanchedAlmond;
   FastLED.show();

   while (true)
   {
      reconnect();
      client.loop();
   }
}

void loop()
{
}
