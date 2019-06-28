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



