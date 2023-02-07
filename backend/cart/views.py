import io
from django.http import FileResponse

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def generate_pdf(title, ingredient_list, filename):
    MIN_ADDITION_SPACES = 3

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, bottomup=0)
    pdfmetrics.registerFont(TTFont('Russian', 'RobotoMono-Regular.ttf'))

    p.setFont('Russian', 16)
    p.drawString(60, 50, title.encode('utf-8'))
    p.line(60, 55, 530, 55)

    p.setFont('Russian', 12)
    text_object = p.beginText(60, 80)
    max_line_length = 0
    for name, volume in ingredient_list:
        max_line_length = max(
            max_line_length,
            len(f'{name}{volume}') + MIN_ADDITION_SPACES
        )
    for name, volume in ingredient_list:
        additional_spaces = max_line_length - len(f'{name}{volume}')
        text_object.textLine(
            f'{chr(2610)} {name}:{"_" * additional_spaces}{volume}'
            .encode('utf-8')
        )
    p.drawText(text_object)

    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=filename)


def generate_ingredient_list(user):
    recipes = user.cart.recipes.all()

    ingredient_list = {}
    for recipe in recipes:
        for ingredient in recipe.ingredients.select_related('ingredient'):
            ingredient_list[str(ingredient.ingredient)] = (
                ingredient_list.get(str(ingredient.ingredient), 0)
                + ingredient.amount)

    return sorted(ingredient_list.items())


def generate_shopping_cart_pdf(user):
    return generate_pdf(
        title=f"{user.first_name}'s shopping cart",
        ingredient_list=generate_ingredient_list(user),
        filename='shopping_cart.pdf'
    )
