## Informacje o projekcie.

Autor: Michał Horodecki

Data: Czerwiec 2019

Projekt jest prezentacją w ramach Regionalnego Programu Stypendialnego 2018 / 2019

Tytuł: Rakiety Genetyczne

Cel: Przedstawienie algorytmu genetycznego na przykładzie ewoluujących rakiet

## Algorytmy Genetyczne

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
3. Geny rakiety reprezentują wartość kąta obrotu
4. W i-tym kroku rakieta obraca się o wartość i-tego genu a następnie przesuwa się w przód.
5. Oceniamy rakietę na podstawie jej odległości do celu.



### Środowisko 
Projekt wykonany został w języku [Python 3.7.0](python.org) z użyciem biblioteki [PyGame](pygame.org), którą można zainstalować poleceniem: `pip install pygame` w konsoli systemowej.


### Pierwsze linie kodu

Zaczniemy od załączenia odpowiednich bibliotek, które będą nam potrzebne.
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

Geny zdają się być najbardziej podstawową rzeczą, dlatego od nich zacznijmy.
Chcemy, aby geny były losową tablicą pewnej liczby liczb rzeczywistych.

```python
def __init__(self, size):
  self.size = size
  self.genes = [self.randGene() for _ in range(size)]
  
def randGene(self):
  return random.random()
```

```python
self.genes = [self.randGene() for _ in range(size)]
```
Powyższa składnia może wyglądać nieco dziwnie dla osób nieobeznanych z Pythonem.
Jest to skrócony zapis wygenerowania tablicy za pomocą danej funkcji.

Słowo kluczowe `self` informuje, że odnosimy się do własności pojedynczego obiektu.

Nasza tablica ma zawierać losowe geny, zatem tworzymy odpowiednią funkcję.
Funkcja `random.random()` zwróci wartość z zakresu `[0, 1]`

Następnie stwórzmy funkcję, która łączy dwa zestawy genów w nowy.
Geny definiują nam ścieżkę rakiety, dlatego wygodnie będzie, gdy nowa ścieżka będzie średnią rodziców.
Po skrzyżowaniu, chcemy zastosować mutację - z pewnym prawdopodobieństwem zmienić geny z pewną siłą.

```python
def cross(self, other):
  new = Genes()
  #Skrzyżuj dwie pary genomów
  for i in range(self.size):
    new.genes[i] = (self.genes[i] + other.genes[i]) / 2
  
  #Zastosuj mutację
  new.mutate(MUTATION_CHANCE, MUTATION_FORCE)
  return new
```

Następnie stwórzmy funkcję mutacji:
```python
def mutate(chance, force):
  for i in range(self.size):
    if random.random() < chance:
      self.genes[i] += random.random() * force
```

Dodajmy zatem zaraz pod dołączeniem bibliotek definicje stałych:
```python
MUTATION_CHANCE = 0.001 #Szansa na mutację genu
MUTATION_FORCE = 0.01 #Współczynnik zmiany
```

Klasa genów jest na ten moment gotowa, przejdźmy zatem do ich obsługi, czyli zaprogramujmy naszą rakietę.
Zastanówmy się, jakie własności chcemy jej nadać.

Potrzebujemy czasu działania, który jest jednocześnie długością genomu.
Oczywiście, rakieta musi wiedzieć skąd dokąd ma latać, chcemy zatem podać pozycję startową i końcową.
Ponadto, aby mierzyć odległość potrzebujemy mapy. 
Ostatnią rzeczą podaną do konstruktora będzie zestaw genów rakiety.

Podczas działania będziemy chcieli znać obecny czas, a także obrót oraz wektor reprezentujący zwrot lotu.

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
  self.forward = [0, -1]
  self.rotation = 0 #Kąt w radianach
```

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
  self.rotaion -= angle #Ponieważ obracamy się przeciwnie do wskazówek zegara, to odejmujemy wartość zmiany
```

Aby móc obserwować nasze rakiety i wyświetlić je na ekranie, zdefiniujmy jeszcze funckję `draw`, która na podanym oknie narysuje rakietę.

```python
def draw(self, window):
  #Stwórz prostokąt i wypełnij go kolorem
  rocketSurface = pygame.Surface(ROCKET_SIZE, pygame.SRCALPHA)
  rocketSurface.fill(ROCKET_COLOR)
  
  rotationDegrees = self.rotation * (180 / math.pi) #Pygame przyjmuje wartość kąta w stopniach
  rotatedRocket = pygame.transform.rotate(rocketSurface, rotationDegrees)
  
  drawPosition = [self.position[0], self.position[1]]
  #Wyśrodkowanie
  drawPosition[0] -= rotatedRocket.get_width() / 2
  drawPosition[1] -= rotatedRocket.get_height() / 2
  
  window.blit(rotatedRocket, drawPosition)
```

Dodajmy nowe stałe na górze programu. Rozmiar i kolor ustalamy dowolnie, dla estetyki.
```python
#Kolor i rozmiar rakiety
ROCKET_SIZE = (5, 15)
ROCKET_COLOR = (50, 250, 90, 128)
```

