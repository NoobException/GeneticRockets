## Informacje o projekcie.

Autor: Michał Horodecki

Data: Czerwiec 2019

Projekt jest pracą w ramach Regionalnego Programu Stypendialnego 2018 / 2019

Tytuł Projektu: Rakiety Genetyczne

Cel: Przedstawienie algorytmu genetycznego na przykładzie ewoluujących rakiet

## O algorytmach genetycznych.

### Czym są?

Algorytm genetyczny to rodzaj algorytmu, który przeszukuje rozwiazązania pewnego problemu, wzorując się na ewolucji biologicznej.
Opiera się na stworzeniu pewnej populacji rozwiązań, a następnie na zasadach doboru naturalnego, w sposób losowy tworzona jest nowa populacja, która dziedziczy cechy poprzedniej.

### Przebieg klasycznego algorytmu

1. Ustalenie postaci rozwiązania jako genów, które zazwyczaj są ciągiem liczb rzeczywistych.
2. Stworzenie losowej populacji
3. Operacje na genach - skrzyżowanie pary osobników lub mutacja (zmiana wartości)
4. Ocena populacji poprzez zastosowanie pewnej funkcji do każdego osobnika
5. Stworzenie nowej populacji, stosując wynik funkcji jako prawdopodobieństwo wyboru
6. Ewolucja kolejnej populacji - powrót do punktu 3.




## Program

### Założenia programu

1. Mamy dany zbiór rakiet o pewnym czasie działania. Ich celem jest dotarcie do pewnego celu.
2. Rakiety posiadaja silniki sterujące, umożliwiające obrót o dowolny kąt.
3. Każda rakieta posiada geny, które reprezentują wartość kąta obrotu
4. W i-tym kroku rakieta obraca się o wartość i-tego genu a następnie przesuwa się w przód.
5. Oceniamy rakietę na podstawie jej odległości do celu.



### Środowisko 
Projekt wykonany został w języku [Python 3.7.0](python.org) z użyciem biblioteki [PyGame](pygame.org), którą można zainstalować poleceniem: `pip install pygame` w konsoli systemowej.


### Pierwsze linie kodu
W pracy będę zakładał, że Czytelnik posiada podstawową znajomość programowania w języku Python. 
Znajomość biblioteki PyGame nie jest wymagana.

Na samej górze programu dodajmy poniższe linie:
```python3
#!/usr/bin/env python
# -*- coding: utf-8 -*-
```
Pozwolą one na pracę z kodowaniem UTF-8

Kod programu zaczniemy od załączenia odpowiednich bibliotek, które będą nam potrzebne.
Oprócz biblioteki graficznej, użyjemy także generatora liczb pseudolosowych.

```python
import random

import pygame
from pygame.locals import *
```

Następnie stwórzmy klasy, które chcemy używać:

```python
class Genes:
  '''Klasa odpowiedzialna za zarządanie genami'''
  pass

class Rocket:
  '''Klasa odpowiedzialna za cykl życiowy rakiety'''
  pass
  
class Population:
  '''Klasa operująca na zbiorze rakiet'''
  pass

class Map:
  '''Klasa kontrolująca mapę'''
  pass
  
class Application:
  '''Główna klasa aplikacji'''
  pass
 
```

### Geny
Geny zdają się być najbardziej podstawową rzeczą, dlatego od nich zacznijmy.
Chcemy, aby geny były losową tablicą pewnej liczby liczb rzeczywistych.

```python
def __init__(self, size):
  self.size = size
  #Tworzymy tablicę losowych genów
  self.genes = [self.randGene() for _ in range(size)]
  
def randGene(self):
  return random.random()
```

```python
self.genes = [self.randGene() for _ in range(size)]
```

Nasza tablica ma zawierać losowe geny, zatem tworzymy odpowiednią funkcję.
Funkcja `random.random()` zwróci wartość z zakresu `[0, 1]`

Następnie stwórzmy funkcję, która łączy dwa zestawy genów w nowy.
Geny definiują nam ścieżkę rakiety, dlatego wygodnie będzie, gdy nowa ścieżka będzie pomiędzy, a więc średnią rodziców.
Po skrzyżowaniu, chcemy zastosować mutację - z pewnym prawdopodobieństwem zmienić geny z pewną siłą.

```python
def cross(self, other):
  new = Genes(self.size)
  #Skrzyżuj dwie pary genomów
  for i in range(self.size):
    new.genes[i] = (self.genes[i] + other.genes[i]) / 2
  
  #Zastosuj mutację
  new.mutate(MUTATION_CHANCE, MUTATION_FORCE)
  return new
```

Następnie stwórzmy funkcję mutacji:
```python
def mutate(self, chance, force):
  for i in range(self.size):
    if random.random() < chance:  
      self.genes[i] += random.random() * force
```

Dodajmy zatem zaraz pod dołączeniem bibliotek definicje stałych:
```python
MUTATION_CHANCE = 0.05 #Szansa na mutację genu
MUTATION_FORCE = 0.02 #Współczynnik zmiany
```

### Rakieta

Klasa genów jest na ten moment gotowa, przejdźmy zatem do ich obsługi, czyli zaprogramujmy naszą rakietę.
Zastanówmy się, jakie własności chcemy jej nadać.

Potrzebujemy czasu działania, który jest jednocześnie długością genomu.
Oczywiście, rakieta musi wiedzieć skąd dokąd ma latać, chcemy zatem podać pozycję startową i końcową, a także geny kontrolujące tor lotu.
Ponadto, aby mierzyć odległość potrzebujemy mapy. 
Podczas działania będziemy chcieli znać obecny czas, a także obrót oraz wektor reprezentujący zwrot lotu.
Rakietę będziemy chcieli oceniać, będziemy więc potrzebowali funkcji liczącej wynik na podstawie odległości.

Nasz konstruktor będzie wyglądał zatem tak:

```python
def __init__(self, lifetime, start, end, map, genes):
  '''
  lifetime - czas działania
  start - pozycja startowa
  end - cel
  map - mapa pozwalająca na obliczenie odległości
  genes - geny dla tej rakiety
  '''
  self.lifetime = lifetime
  self.currentTime = 0
  #Pozycja będzie sie zmieniać, dlatego chcemy skopiować wartości. Inaczej wszystkie rakiety miałyby tę samą pozycję
  self.position = [start[0], start[1]]
  self.target = end
  self.map = map
  self.genes = genes
  
  #Domyślnie rakieta skierowana jest do góry
  self.forward = [0, -ROCKET_FORCE]
  self.rotation = 0 #Kąt w radianach
```

Ustawmy stałą `ROCKET_FORCE = 5` na górze programu

Przejdźmy dalej, do zdefiniowania czynności w każdym kroku.
Na ten moment, chcemy jedynie obrócić rakietę o i-ty kąt, przesunąć się do przodu i przejść do następnego kroku.

```python
def update(self):
  self.rotate(self.geneToAngle(self.genes.genes[self.currentTime]))
  self.move()
  self.currentTime += 1
```
Oczywiście funkcje `rotate`, `geneToAngle` oraz `move` musimy także zdefiniować:

```python
def move(self):
  '''Przesuń rakietę o wektor'''
  self.position[0] += self.forward[0]
  self.position[1] += self.forward[1]
  
def geneToAngle(self, geneValue):
  '''Zamień wartość genu [0,1] na wartość kąta [-0.5, 0.5]. (W radianach)
     Dzięki temu rakieta może się obracać w lewo i w prawo, a ruch jest nieco mniej chaotyczny.'''
  return 0.5 * (geneValue * 2 - 1)
  
def rotate(self, angle):
  '''Obróć rakietę o kąt podany w radianach'''
  x, y = self.forward
  #Używamy tutaj macierzy obrotu
  self.forward[0] = x * math.cos(angle) - y * math.sin(angle)
  self.forward[1] = x * math.sin(angle) + y * math.cos(angle)
  self.rotation -= angle #Ponieważ obracamy się przeciwnie do wskazówek zegara, to odejmujemy wartość zmiany
```

Funkcja `rotate` używa biblioteki `math`, którą musimy dołączyć na górze programu

Aby móc obserwować nasze rakiety i wyświetlić je na ekranie, zdefiniujmy jeszcze funkcję `draw`, która na podanym oknie narysuje rakietę.

```python
def draw(self, window):
  '''Narysuj rakietę w podanym oknie'''
  #Utwórz nowy obszar o rozmiarze ROCKET_SIZE, z włączoną flagą przezroczystości
  rocketSurface = pygame.Surface(ROCKET_SIZE, pygame.SRCALPHA)
  #Wypełniamy go kolorem rakiety
  rocketSurface.fill(ROCKET_COLOR)
  
  rotationDegrees = self.rotation * (180 / math.pi) #Pygame przyjmuje wartość kąta w stopniach
  #Obróć obszar o kąt
  rotatedRocket = pygame.transform.rotate(rocketSurface, rotationDegrees)
  
  drawPosition = [self.position[0], self.position[1]]
  #Wyśrodkowanie
  drawPosition[0] -= rotatedRocket.get_width() / 2
  drawPosition[1] -= rotatedRocket.get_height() / 2
  
  #Umieść obrócony obszar w podanym oknie
  window.blit(rotatedRocket, drawPosition)
```

Dodajmy nowe stałe na górze programu. Rozmiar i kolor ustalamy dowolnie, dla estetyki.
```python
#Kolor i rozmiar rakiety
ROCKET_SIZE = (5, 15)
ROCKET_COLOR = (50, 250, 90, 128)
```

Na koniec dodajmy prostą funkcję liczącą wynik rakiety
```python
def calculateFitness(self):
  return 1 / self.map.getDistance(self.position)
```
Chcemy, żeby wynik był większy im bliżej celu rakieta się znajdzie, dlatego używamy funkcji 1 / x.

### Populacja
Mając rakietę stwórzmy ich populację.

Chcemy, żeby na początku każda rakieta posiadała te same parametry, z wyjątkiem genów.
Zatem populację zaczniemy od ustalenia ilości i paremetrów rakiet.

```python
def __init__(self, rocketCount, rocketLifetime, start, end, map):
  '''
    rocketCount - Ilość rakiet
    rocketLifetime - Czas pracy rakiety
    start - Pozycja startowa
    end - Cel
    map - Mapa
  '''
  self.rocketCount = rocketCount
  self.size = size
  self.rocketLifetime = rocketLifetime
  self.start = start
  self.end = end
  self.map = map
  
  self.rockets = [Rocket(rocketLifetime, start, end, map, Genes())]
  self.generation = 0 # Numer generacji (ilość podejść)
  self.lifeIndex = 0 # Numer genu który przetwarzamy
  
```
Następnie napiszmy dwie proste funkcje, wywoływane co klatkę odpowiedzialne za aktualizowanie i rysowanie populacji:

```python
def update(self):
  '''Zaktualizuj wszystkie rakiety. Jeśli ich czas się skończył, stwórz nową populację'''
  for rocket in self.rockets:
    rocket.update()
  self.lifeIndex += 1
  if self.lifeIndex == self.rocketLifetime:
    self.nextPopulation()
    
def draw(self, window):
  '''Narysuj rakiety na ekranie'''
  for rocket in self.rockets:
    rocket.draw(window)
```

Na koniec pracy z populacją stwórzmy funkcję `nextPopulation`.
Jej zadaniem będzie ocenienie obecnej populacji i bazując na doborze naturalnym, stworzenie nowej.

```python
def nextPopulation(self):
  '''Dla każdej rakiety ustal szansę na wybranie, a następnie stwórz nową, losową populację.'''
  
  # Zaczynamy od policzenia najmniejszego i najmniejszego dopasowania
  # Dzięki temu możemy znormalizować wyniki, aby znajdowały się między 0 a 1
  minFitness = maxFitness = self.rockets[0].calculateFitness()
  for rocket in self.rockets:
    fitness = rocket.calculateFitness()
    minFitness = min(minFitness, fitness)
    maxFitness = max(maxFitness, fitness)
    
  # Normalizujemy wyniki i zamieniamy na szansę wyboru przez dodanie rakiety proporcjonalną ilość razy do puli
  matePool = []
  for rocket in self.rockets:
    fitness = rocket.calculateFitness()
    fitnessNormalized = (fitness - minFitness) / (maxFitness - minFitness + 1) # Dodajemy 1, żeby na pewno nie podzielić przez 0
    matePool += [rocket] * int(fitnessNormalized * 100)
    
  # Resetujemy populacje, losowo wybieramy rodziców, krzyżujemy ich geny i tworzymy nowe rakiety
  self.rockets = []
  for _ in range(self.rocketCount):
    rocketA = random.choice(matePool)
    rocketB = random.choice(matePool)
    newGenes = rocketA.genes.cross(rocketB.genes)
    self.rockets.append(Rocket(self.rocketLifetime, self.start, self.end, self.map, newGenes))
   
  self.generation += 1
  self.lifeIndex = 0
```

### Mapa 
Kolejną rzeczą, której potrzebujemy, jest mapa po której będą się poruszały rakiety
Aby nie komplikować za bardzo, nasza mapa nie będzie zawierała żadnych przeszkód, a jedynie cel
Oczywiście potrzebujemy również funkcji `getDistance` używanej do liczenia wyniku rakiety

```python
def __init__(self, targetPosition):
  self.targetPosition = targetPosition

def getDistance(self, point):
  # Odległość liczymy z twierdzenia Pitagorasa
 return math.sqrt((point[0] - self.targetPosition[0]) ** 2 + (point[1] - self.targetPosition[1]) ** 2) 

def draw(self, window):
  # Narysuj białe kółko w miejscu celu
  pygame.draw.circle(window, (255, 255, 255), self.targetPosition, 10)
```


### Aplikacja
Teraz, gdy mamy już wszystkie elementy, chcemy zebrać je w całość

Aplikacja składa się z okna, populacji, oraz mapy
```python
def __init__(self):
  pygame.init()
  self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
  self.map = Map(TARGET_POSITION)
  self.population = Population(ROCKET_COUNT, ROCKET_LIFETIME, START_POSITION, TARGET_POSITION, self.map);
  self.start()
```

Zapiszmy stałe, których tu używamy, na górze programu

```python
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 640

START_POSITION = (320, 600)
TARGET_POSITION = (320, 50)

ROCKET_COUNT = 100
ROCKET_LIFETIME = 300
```

Następnie napiszmy główną pętlę
```python
def start(self):
  self.running = True
  while self.running:
    self.processEvents()

    self.map.draw(self.window)

    self.population.update()
    self.population.draw(self.window)
    
    pygame.display.update()
    time.sleep(0.001)
```
`time.sleep(0.001)` wywołujemy aby spowolnić nieco aplikację w celu obserwacji,
musimy jednak zaimportować bibliotekę `time`

`pygame.display.update()` jest funkcją biblioteki graficznej, która wyświetla narysowane rzeczy

Musimy także napisać funkcję `processEvents` łącząca naszą aplikację z biblioteką

```python
def processEvents(self):
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      self.running = False
```

Mając aplikację, na samym dole piszemy `Application()` aby ją uruchomić.
Następnie w powłoce systemowej wywołujemy polecenie `python3 [nazwa-pliku]` aby uruchomić program

## Podsumowanie
Program przeze mnie przedstawiony nie jest zbyt złożony, stanowi raczej przykład metody.

Jego funkcjonalność dałoby się rozszerzyć i skalibrować, np. przez
- eksperymentację z systemem genów
- modifykację dziedziczenia
- rozbudowaniem mapy
itp.

Mam nadzieję, że udało mi się Czytelnikowi nieco przybliżyć temat algorytmów genetycznych.

