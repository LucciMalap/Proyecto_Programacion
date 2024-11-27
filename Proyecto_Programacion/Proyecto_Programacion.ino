#define LEDBLANCO1 10
#define LEDBLANCO2 11
#define LEDBLANCO3 12
#define TRIGGER 4
#define ECHO 5
#define BUZZER 6
int Inputs = 0;
int contador = 0;
int tono = 2000;
bool sistemaEncendido = true;

const float sonido = 34300.0;

void setup() {
  Serial.begin(9600);
  
  pinMode(LEDBLANCO1, OUTPUT);
  pinMode(LEDBLANCO2, OUTPUT);
  pinMode(LEDBLANCO3, OUTPUT);
  pinMode(ECHO, INPUT);
  pinMode(TRIGGER, OUTPUT);
  pinMode(BUZZER, OUTPUT);
  
  apagarLEDs();
}

void loop() {
  if (Serial.available() > 0) {
    Inputs = Serial.read();
  }

  switch (Inputs) {
    case 'A':
      sistemaEncendido = false;
      apagarAlertas();
      break;
    case 'B':
      sistemaEncendido = true;
      break;    
    case 'C': 
      tono = 0;
      break;
    case 'D': 
      tono = 500;
      break;
    case 'E':
      tono = 1500;
      break;
    case 'F':
      tono = 2000;
      break;
  }

  if (sistemaEncendido) {
    iniciarTrigger();
    float distancia = calcularDistancia();

    if (distancia < 10) { 
      encenderAlertas();
      Serial.write('S');  // Enviar señal al detectar proximidad
      Serial.println();
    } 
    else {
      apagarAlertas();
    }
  }
}

void apagarAlertas() {
  apagarLEDs();
  noTone(BUZZER);
  delay(200);
}

void encenderAlertas() {
  digitalWrite(LEDBLANCO1, HIGH);
  digitalWrite(LEDBLANCO2, HIGH);
  digitalWrite(LEDBLANCO3, HIGH);
  tone(BUZZER, tono);
  delay(2000);
}

void apagarLEDs() {
  digitalWrite(LEDBLANCO1, LOW);
  digitalWrite(LEDBLANCO2, LOW);
  digitalWrite(LEDBLANCO3, LOW);
}

float calcularDistancia() {
  unsigned long tiempo = pulseIn(ECHO, HIGH);
  float distancia = tiempo * 0.000001 * sonido / 2.0;
  return distancia;
}

void iniciarTrigger() {
  digitalWrite(TRIGGER, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIGGER, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIGGER, LOW);
}
