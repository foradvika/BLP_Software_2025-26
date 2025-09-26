// ------------------- VALVE + ALL DUCERS TEST (only current ducer 3 active) -------------------

// Valve NV_02
int v4 = 21;   // NV_02 pin

// Voltage-output transducers
int ducer1Pin = A8;   // first voltage ducer pin
int ducer2Pin = A10;  // second voltage ducer pin

// Current-output transducers
int currentDucer1Pin = A9;   // first current ducer pin
int currentDucer2Pin = A11;  // second current ducer pin
int currentDucer3Pin = A9;  // third current ducer pin

// Calibration values
float V0 = 0.5;       // sensor min output voltage (V)
float Vmax = 4.5;     // sensor max output voltage (V)
int Pmax = 500;       // max PSI

void setup() {
  // Setup valve pin
  pinMode(v4, OUTPUT);
  
  // Start Serial communication
  Serial.begin(9600);
  delay(2000);  // give time to open Serial Monitor
  
  Serial.println("Starting NV_02 + all ducers test (only current ducer 3 active)...");
}

void loop() { 
  // Read all ducers
  readDucers();

  delay(500);  // half-second delay
}

// ------------------- Function to read all ducers -------------------
void readDucers() {
  /*
  // Voltage Ducer 1
  int raw1 = analogRead(ducer1Pin);
  float voltage1 = raw1 * (5.0 / 1023.0);
  float pressure1 = Pmax * ((voltage1 - V0) / (Vmax - V0)) + 14.7;

  // Voltage Ducer 2
  int raw2 = analogRead(ducer2Pin);
  float voltage2 = raw2 * (5.0 / 1023.0);
  float pressure2 = Pmax * ((voltage2 - V0) / (Vmax - V0)) + 14.7;

  // Current Ducer 1
  int raw3 = analogRead(currentDucer1Pin);
  float voltage3 = raw3 * (5.0 / 1023.0);
  float current1_mA = (voltage3 / 250.0) * 1000.0;
  float pressure3 = Pmax * ((current1_mA - 4.0) / (20.0 - 4.0)) + 14.7 + 10;

  // Current Ducer 2
  int raw4 = analogRead(currentDucer2Pin);
  float voltage4 = raw4 * (5.0 / 1023.0);
  float current2_mA = (voltage4 / 250.0) * 1000.0;
  float pressure4 = Pmax * ((current2_mA - 4.0) / (20.0 - 4.0)) + 14.7 + 30;
  */

  // Current Ducer 3 (active)
  int raw5 = analogRead(currentDucer3Pin);
  float voltage5 = raw5 * (5.0 / 1023.0);
  float current3_mA = (voltage5 / 250.0) * 1000.0;
  float pressure5 = Pmax * ((current3_mA - 4.0) / (20.0 - 4.0)) + 14.7 + 10;

  // Print reading for current ducer 3
  Serial.print("Current Ducer 3 - Current: "); Serial.print(current3_mA, 1); Serial.print(" mA");
  Serial.print("   Pressure: "); Serial.println(pressure5, 1);

  Serial.println("----------------------------------");
}
