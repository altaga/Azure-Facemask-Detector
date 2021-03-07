
#include "esp_camera.h"
#include "Arduino.h"
#include "soc/soc.h"           // Disable brownour problems
#include "soc/rtc_cntl_reg.h"  // Disable brownour problems
#include "driver/rtc_io.h"
#include <EEPROM.h>            // read and write from flash memory
#include <base64.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include "certs.h"
#include <Pushbutton.h>

// Pin definition for CAMERA_MODEL_AI_THINKER
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27
#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

int pictureNumber = 0;
Pushbutton button(12);

void initWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
  }
}

void setup() {
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0); //disable brownout detector
  pinMode(14, OUTPUT);
  pinMode(15, OUTPUT);
  pinMode(13, OUTPUT);
  digitalWrite(14, LOW);
  digitalWrite(15, LOW);
  digitalWrite(13, LOW);
  delay(1000);
  initWiFi();
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  if (psramFound()) {
    config.frame_size = FRAMESIZE_QVGA; // FRAMESIZE_ + QVGA|CIF|VGA|SVGA|XGA|SXGA|UXGA
    config.jpeg_quality = 6;
    config.fb_count = 2;
  } else {
    config.frame_size = FRAMESIZE_QVGA;
    config.jpeg_quality = 6;
    config.fb_count = 1;
  }
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    return;
  }
digitalWrite(13, HIGH);
}

void loop() {
  if ((WiFi.status() == WL_CONNECTED)) {
  if (button.getSingleDebouncedRelease())
  {
    digitalWrite(14, LOW);
    digitalWrite(15, LOW);
    digitalWrite(13, LOW);
    
    camera_fb_t * fb = NULL;
    // Take Picture with Camera
    fb = esp_camera_fb_get();
    if (!fb) {

      return;
    }
    
    String encoded = base64::encode(fb->buf, fb->len);
     //Check the current connection status
      HTTPClient http;
      http.begin("https://facemask-apim.azure-api.net/tensorpython37/HttpTrigger1?flag=read", root_ca); //Specify the URL and certificate
      http.addHeader("Content-Type", "text/plain");
      http.addHeader("Ocp-Apim-Subscription-Key", key);
      int httpCode = http.POST(encoded);
      if (httpCode > 0) {
        String payload = http.getString();
        if (payload == "Facemask OFF")
        {
          digitalWrite(14, HIGH);
        }
        else if (payload == "Facemask ON") {
          digitalWrite(15, HIGH);
        }
        else {
          digitalWrite(13, HIGH);
        }
      }
      else {
        digitalWrite(13, HIGH);
        digitalWrite(15, HIGH);
        digitalWrite(14, HIGH);
      }
      http.end();
    }
  }
  else{
    WiFi.disconnect();
    WiFi.reconnect();
  }
}
