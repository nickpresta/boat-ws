import elixir
from src.models import *

# Creates an empty database and initializes the mapping
elixir.setup_all(True)

if __name__ == '__main__':

    ships = [{'hit_points': 150, 'max_hit_points': 150, 'max_speed': 230, 'num_cannons': 28,
                'ship_type': ShipType.FRIGATE, 'name': u"HMS Surprise",
                'max_theta': 180, 'max_ratio': 2, 'turn_radius_factor': 1,
                'sails': 0.0, 'ammo': 280, 'firing_range': 600, 'firing_rate': 1.5, 'repair_rate': 2.0, 'repairs_available': 5},
            {'hit_points': 100, 'max_hit_points': 100, 'max_speed': 100, 'num_cannons': 28,
                'ship_type': ShipType.FRIGATE, 'name': u"HMS Pollux",
                'max_theta': 180, 'max_ratio': 2, 'turn_radius_factor': 1,
                'sails': 0.0, 'ammo': 200, 'firing_range': 600, 'firing_rate': 1.5, 'repair_rate': 2.0, 'repairs_available': 5},
            {'hit_points': 230, 'max_hit_points': 230, 'max_speed': 180, 'num_cannons': 80,
                'ship_type': ShipType.MAN_OF_WAR, 'name': u"Mistral",
                'max_theta': 180, 'max_ratio': 2, 'turn_radius_factor': 1,
                'sails': 0.0, 'ammo': 100, 'firing_range': 600, 'firing_rate': 1.5, 'repair_rate': 1.0, 'repairs_available': 5},
            {'hit_points': 150, 'max_hit_points': 150, 'max_speed': 200, 'num_cannons': 38,
                'ship_type': ShipType.FRIGATE, 'name': u"Redoubtable",
                'max_theta': 180, 'max_ratio': 2, 'turn_radius_factor': 1,
                'sails': 0.0, 'ammo': 100, 'firing_range': 600, 'firing_rate': 1.5, 'repair_rate': 2.0, 'repairs_available': 5},
            {'hit_points': 150, 'max_hit_points': 150, 'max_speed': 230, 'num_cannons': 28,
                'ship_type': ShipType.FRIGATE, 'name': u"Voorzichtigheid",
                'max_theta': 180, 'max_ratio': 2, 'turn_radius_factor': 1,
                'sails': 0.0, 'ammo': 100, 'firing_range': 600, 'firing_rate': 1.5, 'repair_rate': 2.0, 'repairs_available': 5},
            {'hit_points': 160, 'max_hit_points': 160, 'max_speed': 250, 'num_cannons': 14,
                'ship_type': ShipType.BRIG, 'name': u"HMS Sophie",
                'max_theta': 180, 'max_ratio': 2, 'turn_radius_factor': 1,
                'sails': 0.0, 'ammo': 100, 'firing_range': 600, 'firing_rate': 1.5, 'repair_rate': 3.0, 'repairs_available': 5},
            {'hit_points': 120, 'max_hit_points': 120, 'max_speed': 320, 'num_cannons': 7,
                'ship_type': ShipType.PRIVATEER, 'name': u"Felipe V",
                'max_theta': 180, 'max_ratio': 2, 'turn_radius_factor': 1,
                'sails': 0.0, 'ammo': 100, 'firing_range': 600, 'firing_rate': 1.5, 'repair_rate': 4.0, 'repairs_available': 5},
            {'hit_points': 150, 'max_hit_points': 150, 'max_speed': 250, 'num_cannons': 30,
                'ship_type': ShipType.FRIGATE, 'name': u"HMS Worchester",
                'max_theta': 180, 'max_ratio': 2, 'turn_radius_factor': 1,
                'sails': 0.0, 'ammo': 100, 'firing_range': 600, 'firing_rate': 1.5, 'repair_rate': 2.0, 'repairs_available': 5},
            {'hit_points': 150, 'max_hit_points': 150, 'max_speed': 220, 'num_cannons': 28,
                'ship_type': ShipType.FRIGATE, 'name': u"Jemmapes",
                'max_theta': 180, 'max_ratio': 2, 'turn_radius_factor': 1,
                'sails': 0.0, 'ammo': 100, 'firing_range': 600, 'firing_rate': 1.5, 'repair_rate': 2.0, 'repairs_available': 5},
            {'hit_points': 150, 'max_hit_points': 150, 'max_speed': 250, 'num_cannons': 22,
                'ship_type': ShipType.CORVETTE, 'name': u"HMS Ariel",
                'max_theta': 180, 'max_ratio': 2, 'turn_radius_factor': 1,
                'sails': 0.0, 'ammo': 100, 'firing_range': 600, 'firing_rate': 1.5, 'repair_rate': 3.0, 'repairs_available': 5},
            {'hit_points': 120, 'max_hit_points': 120, 'max_speed': 350, 'num_cannons': 14,
                'ship_type': ShipType.MERCHANT, 'name': u"Minnie",
                'max_theta': 180, 'max_ratio': 2, 'turn_radius_factor': 1,
                'sails': 0.0, 'ammo': 100, 'firing_range': 600, 'firing_rate': 1.5, 'repair_rate': 4.0, 'repairs_available': 5},
            {'hit_points': 250, 'max_hit_points': 250, 'max_speed': 200, 'num_cannons': 70,
                'ship_type': ShipType.MAN_OF_WAR, 'name': u"Meduse",
                'max_theta': 180, 'max_ratio': 2, 'turn_radius_factor': 1,
                'sails': 0.0, 'ammo': 100, 'firing_range': 600, 'firing_rate': 1.5, 'repair_rate': 4.0, 'repairs_available': 5},
            {'hit_points': 150, 'max_hit_points': 150, 'max_speed': 220, 'num_cannons': 38,
                'ship_type': ShipType.CORVETTE, 'name': u"HMS Java",
                'max_theta': 180, 'max_ratio': 2, 'turn_radius_factor': 1,
                'sails': 0.0, 'ammo': 100, 'firing_range': 600, 'firing_rate': 1.5, 'repair_rate': 3.0, 'repairs_available': 5},
            {'hit_points': 150, 'max_hit_points': 150, 'max_speed': 200, 'num_cannons': 44,
                'ship_type': ShipType.FRIGATE, 'name': u"USS Constitution",
                'max_theta': 180, 'max_ratio': 2, 'turn_radius_factor': 1,
                'sails': 0.0, 'ammo': 100, 'firing_range': 600, 'firing_rate': 1.5, 'repair_rate': 2.0, 'repairs_available': 5},
            {'hit_points': 150, 'max_hit_points': 150, 'max_speed': 180, 'num_cannons': 50,
                'ship_type': ShipType.FRIGATE, 'name': u"HMS Leopard",
                'max_theta': 180, 'max_ratio': 2, 'turn_radius_factor': 1,
                'sails': 0.0, 'ammo': 100, 'firing_range': 600, 'firing_rate': 1.5, 'repair_rate': 2.0, 'repairs_available': 5},
            {'hit_points': 230, 'max_hit_points': 230, 'max_speed': 230, 'num_cannons': 56,
                'ship_type': ShipType.MAN_OF_WAR, 'name': u"Waakzambeid",
                'max_theta': 180, 'max_ratio': 2, 'turn_radius_factor': 1,
                'sails': 0.0, 'ammo': 100, 'firing_range': 550, 'firing_rate': 1.5, 'repair_rate': 4.0, 'repairs_available': 5},
            {'hit_points': 150, 'max_hit_points': 150, 'max_speed': 230, 'num_cannons': 26,
                'ship_type': ShipType.FRIGATE, 'name': u"HMS Sirius",
                'max_theta': 180, 'max_ratio': 2, 'turn_radius_factor': 1,
                'sails': 0.0, 'ammo': 100, 'firing_range': 600, 'firing_rate': 1.5, 'repair_rate': 2.0, 'repairs_available': 5},
            {'hit_points': 150, 'max_hit_points': 150, 'max_speed': 200, 'num_cannons': 48,
                'ship_type': ShipType.FRIGATE, 'name': u"Minerve",
                'max_theta': 180, 'max_ratio': 2, 'turn_radius_factor': 1,
                'sails': 0.0, 'ammo': 100, 'firing_range': 600, 'firing_rate': 1.5, 'repair_rate': 2.0, 'repairs_available': 5},
            {'hit_points': 165, 'max_hit_points': 160, 'max_speed': 100, 'num_cannons': 50,
                 'ship_type': ShipType.GALLEON, 'name': u"HMS Kitabi",
                 'max_theta': 180, 'max_ratio': 2, 'turn_radius_factor': 1,
                 'sails': 0.0, 'ammo': 150, 'firing_range': 600, 'firing_rate': 1.5, 'repair_rate': 5.0, 'repairs_available': 5},
            {'hit_points': 200, 'max_hit_points': 200, 'max_speed': 400, 'num_cannons': 34,
                 'ship_type': ShipType.PRIVATEER, 'name': u"Bellone",
                 'max_theta': 180, 'max_ratio': 2, 'turn_radius_factor': 1,
                 'sails': 0.0, 'ammo': 200, 'firing_range': 600, 'firing_rate': 1.5, 'repair_rate': 4.0, 'repairs_available': 5},
            {'hit_points': 230, 'max_hit_points': 230, 'max_speed': 100, 'num_cannons': 40,
                 'ship_type': ShipType.MAN_OF_WAR, 'name': u"HMS Lord Nelson",
                 'max_theta': 180, 'max_ratio': 2, 'turn_radius_factor': 1,
                 'sails': 0.0, 'ammo': 200, 'firing_range': 600, 'firing_rate': 1.5, 'repair_rate': 4.0, 'repairs_available': 5},
            {'hit_points': 150, 'max_hit_points': 150, 'max_speed': 350, 'num_cannons': 22,
                 'ship_type': ShipType.CORVETTE, 'name': u"Berceau",
                 'max_theta': 180, 'max_ratio': 2, 'turn_radius_factor': 1,
                 'sails': 0.0, 'ammo': 50, 'firing_range': 600, 'firing_rate': 1.5, 'repair_rate': 2.0, 'repairs_available': 5}]

    maps = [{'name': u"Summoner's Rift", 'x': 1000, 'y': 1000, 'wind_speed': 25,
                'wind_dir': 0, 'rain': 0.0, 'fog': 300, 'waves': 0.0},
            {'name': u"Port de Barcelona", 'x': 1000, 'y': 1000, 'wind_speed': 25,
                'wind_dir': 270, 'rain': 0.0, 'fog': 300, 'waves': 0.0},
            {'name': u"Treason's Harbour", 'x': 1000, 'y': 1000, 'wind_speed': 30,
                'wind_dir': 135, 'rain': 0.0, 'fog': 300, 'waves': 0.0},
            {'name': u"Medina", 'x': 1000, 'y': 1000, 'wind_speed': 25,
                'wind_dir': 0, 'rain': 0.0, 'fog': 300, 'waves': 0.0},
            {'name': u"Baltic Sea", 'x': 1000, 'y': 1000, 'wind_speed': 15,
                'wind_dir': 90, 'rain': 0.0, 'fog': 300, 'waves': 0.0},
            {'name': u"English Channel", 'x': 1000, 'y': 1000, 'wind_speed': 25,
                'wind_dir': 45, 'rain': 1.0, 'fog': 300, 'waves': 0.0},
            {'name': u"Brazilian Coast", 'x': 1000, 'y': 1000, 'wind_speed': 10,
                'wind_dir': 45, 'rain': 0.5, 'fog': 300, 'waves': 0.0},
            {'name': u"Desolation Island", 'x': 1000, 'y': 1000, 'wind_speed': 25,
                'wind_dir': 180, 'rain': 0.5, 'fog': 300, 'waves': 0.0},
            {'name': u"Ile de la Passe", 'x': 1000, 'y': 1000, 'wind_speed': 25,
                'wind_dir': 315, 'rain': 0.5, 'fog': 300, 'waves': 0.0},
            {'name': u"Cape Vendres", 'x': 1000, 'y': 1000, 'wind_speed': 25,
                'wind_dir': 45, 'rain': 0.5, 'fog': 300, 'waves': 0.0},
            {'name': u"Bay of Bengal", 'x': 1000, 'y': 1000, 'wind_speed': 20,
                'wind_dir': 0, 'rain': 0.5, 'fog': 300, 'waves': 0.0},
            {'name': u"Bay of Biscay", 'x': 1000, 'y': 1000, 'wind_speed': 15,
                'wind_dir': 225, 'rain': 0.5, 'fog': 300, 'waves': 0.0}]

    # get the name of all ships in the DB
    all_ships = [s.name for s in Ship.query.all()]
    all_maps = [m.name for m in Map.query.all()]

    # insert dummy data
    for s in ships:
        # if the ship doesn't exist
        if s['name'] not in all_ships:
            Ship(**s)

    for m in maps:
        # if the map doesn't exist
        if m['name'] not in all_maps:
            Map(**m)

    # commit
    elixir.session.commit()

    print "Database contains:"
    for s in Ship.query.all():
        print "\t%s" % s
    for m in Map.query.all():
        print "\t%s" % m
