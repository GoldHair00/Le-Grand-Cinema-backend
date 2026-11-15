
from datetime import datetime, timedelta

from app import create_app
from app.extensions import db
from app.models import Film, Room, Seat, Screening


app = create_app()

with app.app_context():
    # 1. Créer les films s'ils n'existent pas
    films_data = [
        ("Le Voyage", "Un grand voyage inattendu.", 110),
        ("Les Étoiles", "Une aventure sous les étoiles.", 125),
        ("Le Dernier Secret", "Un mystère à résoudre.", 95),
        ("Harry Potter et le Prince de sang-mêlé", "Harry Potter découvre les secrets du passé de Voldemort.", 153),
        ("Princesse Mononoké",
         "Une jeune guerrière se retrouve au cœur d'un conflit entre humains et esprits de la forêt.", 134),
        ("Your Name", "Deux adolescents échangent mystérieusement leurs corps à distance.", 106),
    ]
    films = {}

    for title, description, duration in films_data:
        film = Film.query.filter_by(title=title).first()

        if film is None:
            film = Film(
                title=title,
                description=description,
                duration_minutes=duration,
            )
            db.session.add(film)

        films[title] = film

    # 2. Créer les salles
    rooms = {}

    for name in ["Salle 1", "Salle 2"]:
        room = Room.query.filter_by(name=name).first()

        if room is None:
            room = Room(name=name)
            db.session.add(room)

        rooms[name] = room

    db.session.flush()

    # 3. Créer les sièges : 4 rangées de 6 places
    for room in rooms.values():
        for row in ["A", "B", "C", "D"]:
            for number in range(1, 7):
                seat = Seat.query.filter_by(
                    room_id=room.id,
                    row_label=row,
                    number=number,
                ).first()

                if seat is None:
                    db.session.add(
                        Seat(
                            room_id=room.id,
                            row_label=row,
                            number=number,
                        )
                    )

    # 4. Créer trois séances pour demain
    tomorrow = datetime.now().date() + timedelta(days=1)

    screenings_data = [
        ("Le Voyage", "Salle 1", 14, 0),
        ("Les Étoiles", "Salle 1", 17, 0),
        ("Le Dernier Secret", "Salle 2", 20, 0),
        ("Harry Potter et le Prince de sang-mêlé", "Salle 1", 15, 30),
        ("Princesse Mononoké", "Salle 2", 18, 0),
        ("Your Name", "Salle 1", 20, 0),
    ]

    for film_title, room_name, hour, minute in screenings_data:
        starts_at = datetime.combine(
            tomorrow,
            datetime.min.time().replace(hour=hour, minute=minute),
        )

        film = films[film_title]
        room = rooms[room_name]

        screening = Screening.query.filter_by(
            film_id=film.id,
            room_id=room.id,
            starts_at=starts_at,
        ).first()

        if screening is None:
            db.session.add(
                Screening(
                    film_id=film.id,
                    room_id=room.id,
                    starts_at=starts_at,
                    price=12.00,
                )
            )

    db.session.commit()

    print("Données de démonstration créées ou déjà présentes.")
    print(f"Films : {Film.query.count()}")
    print(f"Salles : {Room.query.count()}")
    print(f"Sièges : {Seat.query.count()}")
    print(f"Séances : {Screening.query.count()}")
