import random, time, json, math, logging
from typing import List, Dict
from functools import lru_cache

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("GalacticSim")

class ResourceNotFound(Exception): pass

class Resource:
    def __init__(self, name: str, base_price: float):
        self.name = name
        self.base_price = base_price

    def price_fluctuation(self):
        return round(self.base_price * random.uniform(0.8, 1.2), 2)

class Planet:
    def __init__(self, name: str, richness: float, population: int):
        self.name = name
        self.richness = richness
        self.population = population
        self.resources: Dict[str, float] = {}
        self._generate_resources()

    def _generate_resources(self):
        for res in ["metal", "gas", "spice", "water"]:
            self.resources[res] = max(0.1, self.richness * random.uniform(0.5, 2))

    def consume(self, resource: str, amount: float):
        if self.resources.get(resource, 0) < amount:
            raise ResourceNotFound(f"{self.name} lacks {resource}")
        self.resources[resource] -= amount

    def produce(self, resource: str, amount: float):
        self.resources[resource] = self.resources.get(resource, 0) + amount

    def __repr__(self):
        return f"<Planet {self.name} pop={self.population} res={self.resources}>"

class TradeRoute:
    def __init__(self, source: Planet, target: Planet, resource: str):
        self.source = source
        self.target = target
        self.resource = resource
        self.distance = self.compute_distance()

    def compute_distance(self):
        return random.uniform(1.0, 100.0)

    def transfer(self):
        try:
            amt = min(5.0, self.source.resources.get(self.resource, 0))
            if amt <= 0:
                return 0
            self.source.consume(self.resource, amt)
            self.target.produce(self.resource, amt)
            logger.info(f"{amt} {self.resource} transferred {self.source.name} -> {self.target.name}")
            return amt
        except ResourceNotFound as e:
            logger.warning(str(e))
            return 0

class Galaxy:
    def __init__(self, n=5):
        self.planets = [Planet(f"Planet-{i}", random.uniform(0.5, 2.0), random.randint(1000, 1000000)) for i in range(n)]
        self.routes: List[TradeRoute] = []
        self.resources = [Resource("metal", 10), Resource("gas", 20), Resource("spice", 100), Resource("water", 5)]
        self._generate_routes()

    def _generate_routes(self):
        for _ in range(10):
            p1, p2 = random.sample(self.planets, 2)
            r = random.choice(["metal", "gas", "spice", "water"])
            self.routes.append(TradeRoute(p1, p2, r))

    def tick(self):
        logger.info("=== GALAXY TICK ===")
        for r in self.routes:
            r.transfer()
        self._update_prices()
        self._simulate_population()

    @lru_cache(maxsize=16)
    def get_resource_price(self, name: str):
        for r in self.resources:
            if r.name == name:
                return r.price_fluctuation()
        raise ResourceNotFound(name)

    def _update_prices(self):
        for r in self.resources:
            price = r.price_fluctuation()
            logger.info(f"Market update: {r.name} = {price} credits")

    def _simulate_population(self):
        for p in self.planets:
            growth = int(p.population * random.uniform(-0.01, 0.02))
            p.population += growth
            logger.info(f"{p.name} population change: {growth:+}")

    def save_state(self, file="galaxy.json"):
        state = {
            "planets": [{
                "name": p.name,
                "population": p.population,
                "richness": p.richness,
                "resources": p.resources
            } for p in self.planets]
        }
        with open(file, "w") as f:
            json.dump(state, f, indent=2)

    def load_state(self, file="galaxy.json"):
        with open(file) as f:
            state = json.load(f)
        self.planets = []
        for pd in state["planets"]:
            p = Planet(pd["name"], pd["richness"], pd["population"])
            p.resources = pd["resources"]
            self.planets.append(p)

if __name__ == "__main__":
    g = Galaxy(n=8)
    for _ in range(5):
        g.tick()
        time.sleep(1)
    g.save_state()
