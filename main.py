from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

# Create database
Base = declarative_base()


class Flashcard(Base):
    __tablename__ = 'flashcard'

    id = Column(Integer, primary_key=True)
    question = Column(String(50), nullable=False)
    answer = Column(String(50), nullable=False)
    box_number = Column(Integer, default=0, nullable=False)

    def __repr__(self) -> str:
        return f"Flashcard(id={self.id}, question={self.question}, " \
               f"answer={self.answer}, box_number={self.box_number}"


engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')
Base.metadata.create_all(engine)


# Menu
def main():
    print("1. Add flashcards\n"
          "2. Practice flashcards\n"
          "3. Exit")
    menu_choice = input()
    if menu_choice == '1':
        add_flashcards()
    elif menu_choice == '2':
        session = Session(engine)
        all_flashcards_list = session.query(Flashcard).all()
        flashcards = [{flashcard.question: flashcard.answer} for flashcard in all_flashcards_list]

        if flashcards:
            for flash in flashcards:
                for question, answer in flash.items():
                    print(f'Question: {question}')
                    print('press "y" to see the answer:\n'
                          'press "n" to skip:\n'
                          'press "u" to update:\n')
                    choice = input()
                    if choice == 'y':
                        print(f'Answer: {answer}')
                        print('press "y" if your answer is correct:\n'
                              'press "n" if your answer is wrong:')
                        y_choice = input()
                        if y_choice == 'y':
                            query = session.query(Flashcard)
                            query.filter(Flashcard.question == question).update(
                                {Flashcard.box_number: Flashcard.box_number + 1})
                            if query.filter(Flashcard.question == question).first().box_number >= 3:
                                query.filter(Flashcard.question == question).delete()
                            session.commit()
                        elif y_choice == 'n':
                            continue

                    elif choice == 'n':
                        continue
                    elif choice == 'u':
                        print('press "d" to delete the flashcard:\n'
                              'press "e" to edit the flashcard:')
                        u_choice = input()
                        if u_choice == 'd':
                            query = session.query(Flashcard)
                            query.filter(Flashcard.question == question).delete()
                            session.commit()
                        elif u_choice == 'e':
                            query = session.query(Flashcard)
                            print(f'current question: {question}\n'
                                  f'please write a new question:')
                            q = input()
                            print(f'current answer: {answer}\n'
                                  f'please write a new answer:')
                            a = input()
                            query.update({'question': q, 'answer': a})
                            session.commit()
                    else:
                        print(f"{choice} is not an option")
            main()
        else:
            print("There is no flashcard to practice!")
            main()

    elif menu_choice == '3':
        print('Bye!')
    else:
        print(f'{menu_choice} is not an option')
        main()


def add_flashcards():
    print("1. Add a new flashcard\n"
          "2. Exit")
    choice = input()
    if choice == '1':
        question, answer = "", ""
        while not question:
            question = input("Question:\n").strip()
        while not answer:
            answer = input("Answer:\n").strip()
        session = Session(engine)
        new_flashcard = Flashcard(question=question, answer=answer)
        session.add(new_flashcard)
        session.commit()
        add_flashcards()

    elif choice == '2':
        main()
    else:
        print(f'{choice} is not an option')
        add_flashcards()


if __name__ == '__main__':
    main()
