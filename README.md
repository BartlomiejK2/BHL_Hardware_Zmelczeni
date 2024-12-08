# Stellar Companion

## Wprowadzenie

Inteligentny system monitorowania zdrowia fizycznego i psychicznego użytkownika w przestrzeni koszmicznej, zintegrowany z jego strojem. 

## Konstrukcja mechaniczna:
![alt text](https://github.com/BartlomiejK2/BHL_Hardware_Zmelczeni/blob/main/462559004_1541827863141474_5801760832243812464_n.png)

## Układy elektorniczne

System składa się z:
- Raspberry Pi 4B
- Kamera HD B OV5647 5Mpx
- Czujnik Gazu MQ-9
- Czujnik pulsu KY-039
- Inertial Measurement Unit z czujnikiem temperatury MPU6050

Schemat hardware'u znajduje się na poniższym rysunku:
![alt text](https://github.com/BartlomiejK2/BHL_Hardware_Zmelczeni/blob/main/hardware.png)

## Oprogramowanie:

Oprogramowanie systemu podzielone jest na trzy, współdziałające części:
- Oprogramowanie Raspberry Pi
- Oprogramowanie ESP32
- Aplikacja moblina na system Android

Oprogramowanie Raspberry Pi obsługuje IMU, kamerę oraz otrzymuje komunikaty po porcie szeregowym z ESP32. Jego dodatkowym zadaniem jest analizowanie otrzymanych danych z czujników i kamery do wysyłania ich do zdalnego serwera. Najbardziej zaawansowaną częścią tego oprogramowania to model sztucznej inteligencji, który na podstawie wyrazu twarzy jest w stanie określić stan psychiczny użytkownika.

Oprogramowanie ESP32 dotyczy odbierania, przetwarzania i wysyłania danych do Raspberry Pi z czujnika gazu oraz pulsu. Jako, że Raspberry Pi jest przeciążona przez system AI, potrzebowaliśmy dodatkowego układu, który z dużą częstotliwością może przetwarzać analogowe sygnały z czujników.

Aplikacja mobilna jest końcową częścią projektu, składa się z prostego GUI, na którym wyświetleni są astronauci/kosmiczni tyruści, a przy nich wyświetlane są informacje o ich stanie. 

Schemat komunikacyjny między Stellar Companionem (naszym systemem), serwerem przetwarzającym dane oraz aplikacją zaprezentowano poniżej:

![alt text](https://github.com/BartlomiejK2/BHL_Hardware_Zmelczeni/blob/main/462571092_584258157296004_516576879629143503_n.png)

GUI aplikacji:
<div align="center">
  <img src="https://github.com/BartlomiejK2/BHL_Hardware_Zmelczeni/blob/main/462568001_1123533142676140_310810992911452213_n.png">
</div>
