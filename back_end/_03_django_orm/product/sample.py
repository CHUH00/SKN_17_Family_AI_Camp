from django.db import models
from datetime import datetime
import random
from product.models import Product, Category, Discount, Review


def create_sample_categories():
    # Category 샘플 데이터
    category_data = [
        {"name": "가전"},
        {"name": "스마트폰/태블릿"},
        {"name": "가구/인테리어"},
        {"name": "패션/의류"},
        {"name": "스포츠/레저"},
    ]

    # Category 생성
    for data in category_data:
        category, created = Category.objects.get_or_create(name=data["name"])
        if created:
            print(f"Created category: {category.name}")
        else:
            print(f"Category already exists: {category.name}")


def create_sample_products():
    # 실제 데이터를 기반으로 한 Product 샘플 데이터
    product_data = [
        {
            "name": "iPhone 15 Pro",
            "description": "애플의 최신 스마트폰, 강력한 A17 Pro 칩셋과 뛰어난 카메라 성능.",
            "price": 1490000,
            "stock": 20,
            "available": True,
        },
        {
            "name": "Galaxy Z Flip5",
            "description": "삼성의 폴더블 스마트폰, 컴팩트한 디자인과 혁신적인 힌지.",
            "price": 1350000,
            "stock": 15,
            "available": True,
        },
        {
            "name": "LG 올레드 TV 55인치",
            "description": "최상의 화질을 제공하는 LG 올레드 TV. 영화 감상에 최적화.",
            "price": 1790000,
            "stock": 10,
            "available": True,
        },
        {
            "name": "Dyson V12 무선청소기",
            "description": "다이슨의 최첨단 무선청소기. 강력한 흡입력과 긴 배터리 수명.",
            "price": 899000,
            "stock": 25,
            "available": True,
        },
        {
            "name": "Nintendo Switch OLED 모델",
            "description": "닌텐도의 인기 있는 게임 콘솔, 선명한 OLED 화면.",
            "price": 419000,
            "stock": 30,
            "available": True,
        },
        {
            "name": "MacBook Air 15인치 M2",
            "description": "애플의 초경량 노트북, M2 칩셋 탑재로 향상된 성능.",
            "price": 1890000,
            "stock": 10,
            "available": True,
        },
        {
            "name": "Sony WH-1000XM5",
            "description": "소니의 프리미엄 노이즈 캔슬링 헤드폰, 뛰어난 음질 제공.",
            "price": 499000,
            "stock": 40,
            "available": True,
        },
        {
            "name": "Canon EOS R6 Mark II",
            "description": "캐논의 풀프레임 미러리스 카메라, 프로급 사진 촬영에 적합.",
            "price": 2790000,
            "stock": 5,
            "available": True,
        },
        {
            "name": "Apple Watch Series 9",
            "description": "애플의 스마트워치, 더 밝은 디스플레이와 혁신적인 기능.",
            "price": 599000,
            "stock": 50,
            "available": True,
        },
        {
            "name": "Samsung Bespoke 냉장고",
            "description": "삼성의 맞춤형 디자인 냉장고, 고급스러운 인테리어 연출.",
            "price": 2990000,
            "stock": 8,
            "available": True,
        },
    ]

    # Product 생성
    for data in product_data:
        product, created = Product.objects.get_or_create(
            name=data["name"],
            defaults={
                "description": data["description"],
                "price": data["price"],
                "stock": data["stock"],
                "available": data["available"],
            },
        )
        if created:
            print(f"Created product: {product.name}")
        else:
            print(f"Product already exists: {product.name}")


def create_sample_reviews():
    # 샘플 Product 데이터 (ID와 매칭)
    products = [
        (1, "iPhone 15 Pro"),
        (2, "Galaxy Z Flip5"),
        (3, "LG 올레드 TV 55인치"),
        (4, "Dyson V12 무선청소기"),
        (5, "Nintendo Switch OLED 모델"),
        (6, "MacBook Air 15인치 M2"),
        (7, "Sony WH-1000XM5"),
        (8, "Canon EOS R6 Mark II"),
        (9, "Apple Watch Series 9"),
        (10, "Samsung Bespoke 냉장고"),
    ]

    # 샘플 리뷰 데이터 (제품 ID별로 0~4개씩 랜덤 생성)
    review_data = {
        1: [
            (1, 5, "살짝 무겁긴 한데, 간지가 장난 아닙니다."),
            (2, 4, "카메라 성능은 최고! 하지만 발열이 좀 있네요."),
            (10, 5, "사진 퀄리티가 대단합니다. 프로급 장비 같아요."),
            (11, 2, "이번 모델은 아쉽네요. 이전 모델이 더 좋았어요ㅠ"),
        ],
        2: [
            (3, 5, "폴더블이라 휴대성 짱! 힌지가 정말 부드럽습니다."),
            (4, 3, "디자인은 예쁜데, 배터리가 빨리 닳아요."),
        ],
        3: [
            (5, 5, "올레드 화질은 정말 최고입니다. 영화 볼 때 몰입감이 대단하네요."),
        ],
        4: [
            (6, 4, "흡입력은 강력하지만 무게가 조금 무겁습니다."),
            (7, 5, "다이슨 청소기 중 가장 만족스러운 모델이에요!"),
        ],
        5: [
            (8, 5, "OLED 화면 너무 선명하고, 게임 플레이하기에 딱이에요!"),
            (9, 4, "휴대 모드가 편리하고 화면도 좋아요."),
            (10, 5, "닌텐도 팬으로서 너무 만족스럽습니다!"),
        ],
        6: [
            (11, 5, "M2 칩셋 정말 빠릅니다. 작업용으로 최고예요."),
        ],
        7: [
            (12, 5, "노이즈 캔슬링이 엄청 강력합니다. 음질도 너무 좋아요."),
            (13, 4, "장시간 사용하면 귀가 좀 아프긴 해요."),
        ],
        9: [
            (15, 5, "손목에 딱 맞고 기능이 정말 많아요. 운동할 때 최고!"),
        ],
        10: [
            (16, 5, "디자인이 집 인테리어랑 너무 잘 어울립니다."),
            (17, 4, "수납공간이 넓고 활용도가 좋아요."),
        ],
    }

    # Review 생성
    for product_id, reviews in review_data.items():
        for review in reviews:
            user_id, rating, comment = review
            Review.objects.create(
                product_id=product_id,
                user_id=user_id,
                rating=rating,
                comment=comment,
                created_at=datetime.now()
            )
            print(f"Review created for Product {product_id} by User {user_id}")


def create_sample_discounts():
    # 샘플 Product 데이터 (ID와 매칭)
    products = [
        (1, "iPhone 15 Pro"),
        (2, "Galaxy Z Flip5"),
        (3, "LG 올레드 TV 55인치"),
        (4, "Dyson V12 무선청소기"),
        (5, "Nintendo Switch OLED 모델"),
    ]

    # 샘플 할인 데이터
    discount_data = [
        {"product_id": 3, "discount_percentage": 10.00, "start_date": "2025-01-05", "end_date": "2025-01-15"},
        {"product_id": 5, "discount_percentage": 15.00, "start_date": "2025-01-10", "end_date": "2025-01-20"},
        {"product_id": 7, "discount_percentage": 20.00, "start_date": "2025-02-01", "end_date": "2025-02-10"},
        {"product_id": 8, "discount_percentage": 5.00, "start_date": "2025-01-12", "end_date": "2025-01-18"},
        {"product_id": 10, "discount_percentage": 25.00, "start_date": "2025-01-15", "end_date": "2025-01-25"},
    ]

    # Discount 생성
    for data in discount_data:
        start_date = datetime.strptime(data["start_date"], "%Y-%m-%d")
        end_date = datetime.strptime(data["end_date"], "%Y-%m-%d")
        Discount.objects.create(
            product_id=data["product_id"],
            discount_percentage=data["discount_percentage"],
            start_date=start_date,
            end_date=end_date,
        )
        print(f"Discount created: {data['discount_percentage']}% off for Product ID {data['product_id']}")


def create_sample_category_products():
    # 샘플 Product 데이터 (ID와 매칭)
    products = [
        (1, "iPhone 15 Pro"),
        (2, "Galaxy Z Flip5"),
        (3, "LG 올레드 TV 55인치"),
        (4, "Dyson V12 무선청소기"),
        (5, "Nintendo Switch OLED 모델"),
        (6, "MacBook Air 15인치 M2"),
        (7, "Sony WH-1000XM5"),
        (8, "Canon EOS R6 Mark II"),
        (9, "Apple Watch Series 9"),
        (10, "Samsung Bespoke 냉장고"),
    ]

    # 샘플 Category 데이터
    categories = [
        {"name": "가전"},
        {"name": "스마트폰/태블릿"},
        {"name": "가구/인테리어"},
        {"name": "패션/액세서리"},
        {"name": "스포츠/레저"},
    ]

    # Category 생성
    for category_data in categories:
        category, _ = Category.objects.get_or_create(name=category_data["name"])

    # Category와 Product 연결 데이터
    category_products = [
        {"category_name": "스마트폰/태블릿", "product_id": 1},
        {"category_name": "스마트폰/태블릿", "product_id": 2},
        {"category_name": "가전", "product_id": 3},
        {"category_name": "가전", "product_id": 4},
        {"category_name": "스포츠/레저", "product_id": 5},
        {"category_name": "가전", "product_id": 6},
        {"category_name": "패션/액세서리", "product_id": 7},
        {"category_name": "스포츠/레저", "product_id": 8},
        {"category_name": "패션/액세서리", "product_id": 9},
        {"category_name": "가구/인테리어", "product_id": 10},
        {"category_name": "가전", "product_id": 7},
        {"category_name": "스마트폰/태블릿", "product_id": 9},
        {"category_name": "스포츠/레저", "product_id": 3},
        {"category_name": "가구/인테리어", "product_id": 8},
        {"category_name": "스마트폰/태블릿", "product_id": 6},
    ]

    # Category와 Product 연결
    for data in category_products:
        category = Category.objects.get(name=data["category_name"])
        category.products.add(data["product_id"])
        print(f"Linked Product ID {data['product_id']} with Category {category.name}")
