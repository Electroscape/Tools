/*==========================================================================================================*/
/*		2CP - TeamEscape - Engineering
 *		by Robert Schloezer
 *
 *		v1.0
 *		- Vier Taster werden durch ein Relay ersetzt
 *		- Zufaellige, unterschiedliche Drück- und Resetzeiten
 *
 */
/*==========================================================================================================*/

const String title = String("BUTTON-TEST v1.0");


/*==DEFINE==================================================================================================*/
// PINS
const byte pin_1        = 4;
const byte pin_2        = 5;
const byte pin_3        = 6;
const byte pin_4        = 7;
const byte pin_list[4]  = {pin_1, pin_2, pin_3, pin_4};

// Min. und Max. Zeiten für Knopfdruck
const int buttonPress_min = 200;
const int buttonPress_max = 2000;

// Min. und Max. Zeiten für Reset
unsigned long restartDelay_val = 0;
const unsigned long restartDelay_min = 1800000;
const unsigned long restartDelay_max = 5400000;

// Min. und Max. Zeite für Zufallscodes
const unsigned long repeatDelay_min = 1100;
const unsigned long repeatDelay_max = 300000;
/*============================================================================================================
//===SETUP====================================================================================================
//==========================================================================================================*/

void setup() {

  Serial.begin(115200);
  print_logo_infos(title);

  pin_init();

  delay(2000);
}

/*============================================================================================================
//===LOOP=====================================================================================================
//==========================================================================================================*/

void loop() {
  Serial.println("Beginne Zyklus");
  int iterationRandom = random(0,20);
  Serial.print("Anzahl der Zufallscodes: "); Serial.println(iterationRandom);
  for (int a=0; a<iterationRandom; a++) {
    Serial.print("Starte Durchgang "); Serial.println(a+1);
    codeRandom();
  }
  Serial.println("Zyklus Ende"); Serial.println();
  Serial.println("Gebe korrekten Code ein");
  codeCorrect_rnd();
  delay(5000);
  Serial.println("Halte Resettaste");
  codeReset_hold();
  restartDelay_val = random(restartDelay_min, restartDelay_max);
  Serial.print("Zeit bis zur nächsten Eingabe: "); Serial.print(restartDelay_val); Serial.println(" Sekunden"); Serial.println();
  delay( restartDelay_val );
}

/*============================================================================================================
//===INIT=====================================================================================================
//==========================================================================================================*/

void pin_init() {
  pinMode(pin_1, OUTPUT);
  pinMode(pin_2, OUTPUT);
  pinMode(pin_3, OUTPUT);
  pinMode(pin_4, OUTPUT);

  Serial.print(F("Ziehe Pins auf HIGH :"));
  digitalWrite(pin_1, HIGH);
  digitalWrite(pin_2, HIGH);
  digitalWrite(pin_3, HIGH);
  digitalWrite(pin_4, HIGH);
  Serial.println(F("ok"));
  Serial.println();
}

/*============================================================================================================
//===FUNCTIONS================================================================================================
//==========================================================================================================*/

void codeRandom() {
  byte indexRandom = 0;
  byte pinRandom = 0;
  unsigned long repeatRandom = 0;

  for (int i=0; i<8; i++) {
    indexRandom = random(0, 3);
    pinRandom = pin_list[indexRandom];

    digitalWrite(pinRandom, LOW);
    delay( random(buttonPress_min, buttonPress_max) );
    digitalWrite(pinRandom, HIGH);
    delay(100);
  }
  repeatRandom = random(repeatDelay_min, repeatDelay_max);
  Serial.print("Zeit bis zur erneuten Codeeingabe: "); Serial.print(repeatRandom/1000); Serial.println(" Sekunden");
  delay(repeatRandom);
}

void codeCorrect_rnd() {
  // Oben
  digitalWrite(pin_1, LOW);
  delay( random(buttonPress_min, buttonPress_max) );
  digitalWrite(pin_1, HIGH);
  delay(100);

  // Unten
  digitalWrite(pin_2, LOW);
  delay( random(buttonPress_min, buttonPress_max) );
  digitalWrite(pin_2, HIGH);
  delay(100);

  // Oben
  digitalWrite(pin_1, LOW);
  delay( random(buttonPress_min, buttonPress_max) );
  digitalWrite(pin_1, HIGH);
  delay(100);

  // Links
  digitalWrite(pin_3, LOW);
  delay( random(buttonPress_min, buttonPress_max) );
  digitalWrite(pin_3, HIGH);
  delay(100);

  // Rechts
  digitalWrite(pin_4, LOW);
  delay( random(buttonPress_min, buttonPress_max) );
  digitalWrite(pin_4, HIGH);
  delay(100);

  // Rechts
  digitalWrite(pin_4, LOW);
  delay( random(buttonPress_min, buttonPress_max) );
  digitalWrite(pin_4, HIGH);
  delay(100);

  // Oben
  digitalWrite(pin_1, LOW);
  delay( random(buttonPress_min, buttonPress_max) );
  digitalWrite(pin_1, HIGH);
  delay(100);
}

void codeReset_hold() {
  // Links
  digitalWrite(pin_3, LOW);
  delay(6000);
  digitalWrite(pin_3, HIGH);
  delay(100);
}

void print_logo_infos(String progTitle) {
  Serial.println(F("+-----------------------------------+"));
  Serial.println(F("|    TeamEscape HH&S ENGINEERING    |"));
  Serial.println(F("+-----------------------------------+"));
  Serial.println();
  Serial.println(progTitle);
  Serial.println();
  Serial.println();
  delay(2000);
}
