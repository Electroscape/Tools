#include <FastLED.h>
#include <Wire.h>

#define NR_OF_LEDS             40
#define LED_STRIP_TYPE         WS2811
#define RFID_1_LED_PIN         9
#define COLOR_ORDER            BRG // BRG
#define STRIPE_CNT             1

// those are the digital pins
int MODE_PINS[3] = {10, 11, 12};
int BRIGHTNESS_PINS[7] = {2, 3, 4, 5, 6, 7};
uint8_t BRIGHTNESS_VALS[5] = {50, 100, 150, 200, 255};

CRGB LED_STRIPE_1[NR_OF_LEDS];

static CRGB LED_STRIPES[STRIPE_CNT] = {LED_STRIPE_1};

void led_set_clrs(int stripe_nr, CRGB clr, int led_cnt) {
    delay(200);
    for(int i = 0; i < led_cnt; i++) {
        switch(stripe_nr) {
            case 0:
                LED_STRIPE_1[i] = clr; break;
            default: Serial.println("wrong led selection"); break;
        }
    }
    FastLED.show();
    delay(10*led_cnt);
}

void led_set_all_clrs(CRGB clr, int led_cnt) {
    for(int stripe_nr=0; stripe_nr<STRIPE_CNT; stripe_nr++) {
        led_set_clrs(stripe_nr, clr, NR_OF_LEDS);
    }
}

void alternate_red_green() {

    for (int led_no=0; led_no<NR_OF_LEDS; led_no++) {
        if (led_no % 2 == 0) {
            LED_STRIPE_1[led_no] = CRGB::Red;
        } else {
            LED_STRIPE_1[led_no] = CRGB::Green;
        }
    }
    FastLED.show();
    delay(10*NR_OF_LEDS);
}

bool LED_init() {

    // we need to do it manually since we cannot define arrays easily for the preprocessor
    LEDS.addLeds<LED_STRIP_TYPE, RFID_1_LED_PIN, COLOR_ORDER>(LED_STRIPE_1, NR_OF_LEDS);
    delay(200);
    //LEDS.addLeds<LED_STRIP_TYPE, RFID_2_LED_PIN, COLOR_ORDER>(LED_STRIPE_2, NR_OF_LEDS);
    LEDS.setBrightness(255);
    led_set_all_clrs(CRGB::Gold, NR_OF_LEDS);

    return true;
}

void get_settings() {

    int modi = 0;
    double brightness = 0;

    for (int sel=0; sel<sizeof(BRIGHTNESS_PINS); sel++) {
        if (digitalRead(BRIGHTNESS_PINS[sel])) {
            brightness += 2* pow(2, (double)sel);
        }
    }
    for (int sel=0; sel<sizeof(MODE_PINS); sel++) {
        if (digitalRead(MODE_PINS[sel])) {
            modi = sel + 1;
            break;
        }
    }

    Serial.println("modi: ");
    Serial.print(modi);
    Serial.println();

    Serial.println("brightness");
    Serial.println((uint8_t)brightness);
    //
    LEDS.setBrightness((uint8_t)brightness);

    switch (modi) {
        case 1:
            led_set_all_clrs(CRGB::Gold, NR_OF_LEDS);
            break;
        case 2:
            led_set_all_clrs(CRGB::Green, NR_OF_LEDS);
            break;
        case 3:
            alternate_red_green();
            break;
        default:
            Serial.println("inactive");
            led_set_all_clrs(CRGB::Black, NR_OF_LEDS);
            break;
    }
}

void setup() {

    Wire.begin();
    Serial.begin(115200);
    LED_init();

    for (int sel=0; sel<sizeof(BRIGHTNESS_PINS); sel++) {
        pinMode(BRIGHTNESS_PINS[sel], INPUT);
    }
    for (int sel=0; sel<sizeof(MODE_PINS); sel++) {
        pinMode(MODE_PINS[sel], INPUT);
    }
}

void loop() {
    get_settings();
    delay(150);
}
