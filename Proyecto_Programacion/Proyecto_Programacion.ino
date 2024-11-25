#define LEDBLANCO1 10
#define LEDBLANCO2 11
#define LEDBLANCO3 12
#define TRIGGER 5
#define ECHO 6
#define BUZZER 9
int Inputs = 0;
int contador = 0;
int brillo = 255;
int brillo_constante = 255;
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
    brillo = Serial.parseInt();
    delay(10); //evita problemas con entradas 
    if (brillo > 0){
      brillo_constante = brillo;
      Serial.println(brillo);
    }
  }

  switch (Inputs) {
    case 'A':
      sistemaEncendido = false;
      apagarAlertas();
      break;
    case 'B':
      sistemaEncendido = true;
      break;
  }

  if (sistemaEncendido) {
    iniciarTrigger();
    float distancia = calcularDistancia();

    if (distancia < 10) { 
      encenderAlertas();
      sumarContador();
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
  tone(BUZZER, 1000);
  delay(2000);
}

void apagarLEDs() {
  digitalWrite(LEDBLANCO1, LOW);
  digitalWrite(LEDBLANCO2, LOW);
  digitalWrite(LEDBLANCO3, LOW);
}

void sumarContador() {
  contador++;
  Serial.print(contador);
  Serial.println();
  delay(1000);
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