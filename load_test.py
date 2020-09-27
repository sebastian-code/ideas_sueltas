import random
import string

from django.contrib.auth import get_user_model

from bootcamp.articles.models import Article
from bootcamp.messager.models import Message
from bootcamp.news.models import News
from bootcamp.notifications.models import Notification, notification_handler
from bootcamp.qa.models import Question, Answer, Vote


def get_random_str(lenght=12):
    return "".join(
        random.choice(string.ascii_lowercase + string.digits + " ")
        for _ in range(lenght)
    )


def get_usr_name(lenght=10):
    return "".join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(lenght)
    )


def get_random_user():
    return get_user_model().objects.order_by("?").first()


def get_random_tags(mnt):
    return [get_random_str(5) for i in range(mnt)]


tag_set = get_random_tags(40)
for i in range(16):
    user_str = get_usr_name()
    try:
        user = get_user_model().objects.create_user(
            username=user_str, email=user_str + "@gmail.com", password="fuckthis"
        )

        print("User created")

    except Exception as e:
        print("Upppssss, an error on user!", e)

try:
    get_user_model().objects.create_user(
        username="maestro", email="maestro@gmail.com", password="fuckthis"
    )
except:
    print("Upppssss, maestro failed.")

for i in range(62):
    try:
        article = Article.objects.create(
            title=get_random_str(23),
            status="P",
            content=get_random_str(random.randint(1023, 3823)),
            user=get_random_user(),
            tags=random.sample(tag_set, 5),
        )

        print("Created article", article.title)

    except Exception as e:
        print("Upppssss, an error on Article!", e)

for q in Article.objects.all():
    tags_list = random.sample(tag_set, random.randint(4, 9))
    [q.tags.add(tag) for tag in tags_list]
    print("Added tag")

for i in range(12):
    for user in get_user_model().objects.all():
        try:
            news = News.objects.create(
                user=user, content=get_random_str(random.randint(25, 123))
            )
            print("Created news", news)

        except Exception as e:
            print("Upppssss, an error on News!", e)

for i in range(News.objects.count() // 2):
    try:
        news = News.objects.filter(reply=False).order_by("?").first()
        print("Answering to", news)
        user = get_random_user()
        text = get_random_str(random.randint(25, 78))
        news.reply_this(user, text)

    except Exception as e:
        print("Upssssss answer failed")

for sender in get_user_model().objects.all():
    try:
        for receiver in (
            get_user_model().objects.all().exclude(username=sender.username)
        ):
            Message.objects.create(
                sender=sender,
                recipient=receiver,
                message=get_random_str(random.randint(25, 900)),
            )
            Message.objects.create(
                sender=receiver,
                recipient=sender,
                message=get_random_str(random.randint(25, 900)),
            )
            print(f"Conversation created between {sender} and {receiver}")

    except Exception as e:
        print("Upssssss message failed")


for user in get_user_model().objects.all():
    try:
        for i in range(4):
            q = Question.objects.create(
                user=user,
                title=get_random_str(19),
                content=get_random_str(1500),
                tags=random.sample(tag_set, random.randint(2, 6)),
            )

            print(f"Somebody asked {q}")

    except Exception as e:
        print("Upssssss question failed")

for q in Question.objects.all():
    tags_list = random.sample(tag_set, random.randint(4, 9))
    [q.tags.add(tag) for tag in tags_list]
    print(f"Tagged {q}")
    for i in range(random.randint(5, 27)):
        try:
            user = (
                get_user_model()
                .objects.exclude(username=q.user.username)
                .order_by("?")
                .first()
            )
            q.votes.update_or_create(
                user=user,
                defaults={"value": bool(random.getrandbits(1))},
            )
            print(f"Voted {q}")

        except Exception as e:
            print("Uppssss, can't vote", e)

        finally:
            q.count_votes()

for q in Question.objects.all():
    try:
        for user in get_user_model().objects.all():
            Answer.objects.create(user=user, question=q, content=get_random_str(280))
            print(f"Answered to {q}")

    except Exception as e:
        print("Uppssss, can't answer", e)
