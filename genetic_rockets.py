"""
Kod projektu "Rakiety Genetyczne"
Stworzone w ramach Regionalnego Programu Stypendialnego 2018 / 2019
"""

# !/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import random
import time

import pygame
from pygame.locals import *

MUTATION_CHANCE = 0.05  # Szansa na mutację genu
MUTATION_FORCE = 0.02  # Współczynnik zmiany

# Kolor i rozmiar rakiety
ROCKET_SIZE = (5, 15)
ROCKET_COLOR = (50, 250, 90, 128)
ROCKET_FORCE = 5

# Rozmiary okna
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 640

# Początek i koniec trasy
START_POSITION = (320, 600)
TARGET_POSITION = (320, 50)

# Rozmiar populacji
ROCKET_COUNT = 100
ROCKET_LIFETIME = 300


class Genes:
    '''Klasa odpowiedzialna za zarządanie genami'''
    def __init__(self, size):
        self.size = size
        # Tworzymy tablicę losowych genów
        self.genes = [self.randGene() for _ in range(size)]

    def randGene(self):
        return random.random()

    def cross(self, other):
        new = Genes(self.size)
        # Skrzyżuj dwie pary genomów
        for i in range(self.size):
            new.genes[i] = (self.genes[i] + other.genes[i]) / 2

        # Zastosuj mutację
        new.mutate(MUTATION_CHANCE, MUTATION_FORCE)
        return new

    def mutate(self, chance, force):
        for i in range(self.size):
            if random.random() < chance:
                self.genes[i] += random.random() * force


class Rocket:
    '''Klasa odpowiedzialna za cykl życiowy rakiety'''
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

        # Pozycja będzie sie zmieniać, dlatego chcemy skopiować wartości.
        # Inaczej wszystkie rakiety miałyby tę samą pozycję
        self.position = [start[0], start[1]]
        self.target = end
        self.map = map
        self.genes = genes

        # Domyślnie rakieta skierowana jest do góry
        self.forward = [0, -ROCKET_FORCE]
        self.rotation = 0  # Kąt w radianach

    def update(self):
        self.rotate(self.geneToAngle(self.genes.genes[self.currentTime]))
        self.move()
        self.currentTime += 1

    def move(self):
        ''' Przesuń rakietę o wektor '''
        self.position[0] += self.forward[0]
        self.position[1] += self.forward[1]

    def geneToAngle(self, geneValue):
        '''
      Zamień wartość genu [0,1] na wartość kąta [-0.5, 0.5]. (W radianach)
      Dzięki temu rakieta może się obracać w lewo i w prawo, 
      a ruch jest nieco mniej chaotyczny.'''
        return 0.5 * (geneValue * 2 - 1)

    def rotate(self, angle):
        '''Obróć rakietę o kąt podany w radianach'''
        x, y = self.forward

        # Używamy tutaj macierzy obrotu
        self.forward[0] = x * math.cos(angle) - y * math.sin(angle)
        self.forward[1] = x * math.sin(angle) + y * math.cos(angle)

        # Ponieważ obracamy się przeciwnie do wskazówek zegara, to odejmujemy wartość zmiany
        self.rotation -= angle

    def draw(self, window):
        '''Narysuj rakietę w podanym oknie'''
        #Utwórz nowy obszar o rozmiarze ROCKET_SIZE, z włączoną flagą przezroczystości
        rocketSurface = pygame.Surface(ROCKET_SIZE, pygame.SRCALPHA)
        #Wypełniamy go kolorem rakiety
        rocketSurface.fill(ROCKET_COLOR)

        rotationDegrees = self.rotation * (
            180 / math.pi)  #Pygame przyjmuje wartość kąta w stopniach
        #Obróć obszar o kąt
        rotatedRocket = pygame.transform.rotate(rocketSurface, rotationDegrees)

        drawPosition = [self.position[0], self.position[1]]
        #Wyśrodkowanie
        drawPosition[0] -= rotatedRocket.get_width() / 2
        drawPosition[1] -= rotatedRocket.get_height() / 2

        #Umieść obrócony obszar w podanym oknie
        window.blit(rotatedRocket, drawPosition)

    def calculateFitness(self):
        return 1 / self.map.getDistance(self.position)


class Population:
    '''Klasa operująca na zbiorze rakiet'''
    def __init__(self, rocketCount, rocketLifetime, start, end, map):
        '''
        rocketCount - Ilość rakiet
        rocketLifetime - Czas pracy rakiety
        start - Pozycja startowa
        end - Cel
        map - Mapa
      '''
        self.rocketCount = rocketCount
        # self.size = size
        self.rocketLifetime = rocketLifetime
        self.start = start
        self.end = end
        self.map = map

        self.rockets = [
            Rocket(rocketLifetime, start, end, map, Genes(rocketLifetime))
        ]
        self.generation = 0  # Numer generacji (ilość podejść)
        self.lifeIndex = 0  # Numer genu który przetwarzamy   pass

    def update(self):
        '''Zaktualizuj wszystkie rakiety. Jeśli ich czas się skończył, stwórz nową populację'''
        for rocket in self.rockets:
            rocket.update()
        self.lifeIndex += 1
        if self.lifeIndex == self.rocketLifetime:
            self.nextPopulation()

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
            fitnessNormalized = (fitness - minFitness) / (
                maxFitness - minFitness + 0.001
            )  # Dodajemy 1, żeby na pewno nie podzielić przez 0
            matePool += [rocket] * int(1 + fitnessNormalized * 100)
        # Resetujemy populacje, losowo wybieramy rodziców, krzyżujemy ich geny i tworzymy nowe rakiety
        self.rockets = []
        for _ in range(self.rocketCount):
            rocketA = random.choice(matePool)
            rocketB = random.choice(matePool)
            newGenes = rocketA.genes.cross(rocketB.genes)
            self.rockets.append(
                Rocket(self.rocketLifetime, self.start, self.end, self.map,
                       newGenes))

        self.generation += 1
        self.lifeIndex = 0

    def draw(self, window):
        '''Narysuj rakiety na ekranie'''
        for rocket in self.rockets:
            rocket.draw(window)


class Map:
    '''Klasa kontrolująca mapę'''
    def __init__(self, targetPosition):
        self.targetPosition = targetPosition

    def getDistance(self, point):
        # Odległość liczymy z twierdzenia Pitagorasa
        return math.sqrt((point[0] - self.targetPosition[0])**2 +
                         (point[1] - self.targetPosition[1])**2)

    def draw(self, window):
        pygame.draw.circle(window, (255, 255, 255), self.targetPosition, 10)


class Application:
    '''Główna klasa aplikacji'''
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.map = Map(TARGET_POSITION)
        self.population = Population(ROCKET_COUNT, ROCKET_LIFETIME,
                                     START_POSITION, TARGET_POSITION, self.map)
        self.start()

    def start(self):
        self.running = True
        while self.running:
            self.window.fill((20, 20, 20))
            self.processEvents()

            self.map.draw(self.window)

            self.population.update()
            self.population.draw(self.window)

            pygame.display.update()
            time.sleep(0.01)

    def processEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False


Application()
