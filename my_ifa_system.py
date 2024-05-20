from typing import List, Dict
import sqlite3


# a class to represent an odu
class OduIfa:
    def __init__(self, odu_name: str, verses: List[str], meanings: List[str], advice: List[str]):
        self.odu_name = odu_name
        self.verses = verses
        self.meanings = meanings
        self.advice = advice


odu_ifa = [
    OduIfa(
        odu_name="eji ogbe",
        verses=[
            '''
            Eji Ogbe ni oruko mi, mo ni oruko ajinde, mo ni oruko alafia,
            Mo ni oruko orogun, mo ni oruko agbada.
            Orunmila ti o gba enikan, ti o ni gbogbo ibi si o.
            Orunmila ni ko si ibi, ko si arun, ko si aisan,
            Eyin ti e ba n gbe aye yin ba ni owo orun, 
            Eyin ti e ba ti n gbe aye yin ba ni owo aiye.
            ''',

        ],
        meanings=[
            '''
            This Odu signifies new beginnings, success, enlightenment, and a connection to
            divine wisdom. This verse speaks about overcoming obstacles and achieving peace 
            and resurrection. This odu emphasizes the power of Orunmila, the deity of wisdom
            and divination.
            ''',

        ],
        advice=['''
        Embrace new beginnings, maintain peace and be peaceful with everybody and pay close attention
        to your health.
        ''']
    ),
    OduIfa(
        odu_name= "oyeku meji",
        verses= [
            '''
            Oyeku Meji ni gba mi l'owo iku
            Ebo ni o se, ki o le b'alafia ni ile aye
            Adifa fun Oyeku Meji
            Ti nlo sode, ti nlo reru
            Oyeku Meji ni gba mi l'owo iku
            Ebo ni o se, ki o le b'alafia ni ile aye
            '''
        ],
        meanings= [
            '''
            Oyeku Meji represents darkness, death, and transformation. 
            It signifies the importance of rituals and sacrifices to avoid 
            negative outcomes and ensure peace and stability in life. 
            This Odu warns against neglecting spiritual obligations and 
            emphasizes the need for constant spiritual vigilance.
            '''
        ],
        advice=[
            '''
            Perform ritual to avoid negative occurrences, avoid taking unnecessary risks that may lead to harm.
            '''
        ]
    ),

]


# SQLite database
def create_database():
    conn = sqlite3.connect('ifa_divination.db')
    c = conn.cursor()

    # Odu ifa table
    c.execute('''
        CREATE TABLE IF NOT EXISTS odu_ifa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            odu_name TEXT NOT NULL,
            verses TEXT NOT NULL,
            meanings TEXT NOT NULL,
            advice TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


create_database()


def insert_odu_ifa(odu_ifa: OduIfa):
    conn = sqlite3.connect('ifa_divination.db')
    c = conn.cursor()

    # Insert Odu Ifa data
    c.execute('''
        INSERT INTO odu_ifa (odu_name, verses, meanings, advice)
        VALUES (?, ?, ?, ?)
    ''', (odu_ifa.odu_name, '\n'.join(odu_ifa.verses), '\n'.join(odu_ifa.meanings), '\n'.join(odu_ifa.advice)))

    conn.commit()
    conn.close()


for odu in odu_ifa:
    insert_odu_ifa(odu)


# get data from my ifa database

def get_all_odu_ifa():
    conn = sqlite3.connect('ifa_divination.db')
    c = conn.cursor()

    # Retrieve all Odu Ifa data
    c.execute('SELECT odu_name, verses, meanings, advice FROM odu_ifa')
    odu_ifa_list = c.fetchall()

    conn.close()

    # Convert data to OduIfa objects
    return [OduIfa(odu_name, verses.split('\n'), meanings.split('\n'), advice.split('\n')) for odu_name, verses, meanings, advice in odu_ifa_list]


def get_odu_ifa_by_name(odu_name: str):
    conn = sqlite3.connect('ifa_divination.db')
    c = conn.cursor()

    # Retrieve Odu Ifa data by name
    c.execute('SELECT odu_name, verses, meanings, advice FROM odu_ifa WHERE odu_name = ?', (odu_name,))
    result = c.fetchone()

    conn.close()

    if result:
        return OduIfa(result[0], result[1].split('\n'), result[2].split('\n'), result[3].split('\n'))
    else:
        return None


all_odu_ifa = get_all_odu_ifa()
for odu in all_odu_ifa:
    print(f"Odu Ifa: {odu.odu_name.capitalize()}")
    print(f"Verses: {', '.join(odu.verses)}")
    print(f"Meanings: {', '.join(odu.meanings)}")
    print(f"Advice: {', '.join(odu.advice)}")
    print()


def main():
    print("Welcome to the Ifa Divination Knowledge Base")
    while True:
        print("\nMenu:")
        print("1. List all Odu Ifa")
        print("2. Get Odu Ifa by Name")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            odu_ifa_list = get_all_odu_ifa()
            for odu in odu_ifa_list:
                print(f"Odu Ifa: {odu.odu_name}")
        elif choice == "2":
            name = input("Enter the name of the Odu Ifa: ").lower()
            odu = get_odu_ifa_by_name(name)
            if odu:
                print(f"Odu Ifa: {odu.odu_name.capitalize()}")
                print("Verses:")
                for verse in odu.verses:
                    print(f" {verse}")
                print("Meanings:")
                for meaning in odu.meanings:
                    print(f" {meaning}")
                print("Advice:")
                for advice in odu.advice:
                    print(f" {advice}")
            else:
                print("Odu Ifa not found")
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
