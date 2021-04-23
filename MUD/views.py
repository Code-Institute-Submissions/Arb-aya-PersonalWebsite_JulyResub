from django.core.serializers import serialize
from django.shortcuts import render, reverse, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
import json

from .models import Character, Item, ItemSettings
from .forms import EditCharacterForm, DisplayCharacterForm
from .helpers import validate_character_form, get_character


@login_required
def view_character(request):
    """
    Allows the user to view or edit their character.
    """

    can_edit = False

    character = get_character(request.user.username)
    if not character:
        character = Character(owner=request.user)
        character.save()

    if character.points > 0:
        can_edit = True

    character_form = DisplayCharacterForm(instance=character)
    context = {"character_form": character_form, "can_edit": can_edit}

    return render(request, "MUD/index.html", context)


@login_required
def edit_character(request):
    """
    Allows the user to spend points upgrading their character

    """
    character = get_character(request.user.username)
    if not character:
        return redirect(reverse("view_character"))

    if character.points == 0:
        return redirect(reverse("view_character"))

    character_form = EditCharacterForm(
        request.POST or None, instance=character
    )

    if request.method == "POST":
        if character_form.has_changed():
            if character_form.is_valid():
                if validate_character_form(
                    request.POST, request.user.username
                ):
                    character_form.save()
                    if character.points == 0:
                        return redirect(reverse("view_character"))

    context = {"character_form": character_form, "respec": False}

    return render(request, "MUD/editCharacter.html", context)


@login_required
def manage_inventory(request):
    """
    Allows the user to manage their inventory and items.

    """

    character = get_character(request.user.username)
    if not character:
        return redirect(reverse("view_character"))

    character_items = list(character.items.all().order_by("item_id"))

    item_ids = [ItemSettings.item_id for ItemSettings in character_items]

    item_data = list(
        Item.objects.filter(pk__in=item_ids)
        .order_by("id")
        .values("name", "image", "item_type", "slot", "width", "height")
    )

    for index, item in enumerate(item_data):
        item["lastSpaceIndex"] = character_items[index].lastSpaceIndex
        item["currentSpaceIndex"] = character_items[index].currentSpaceIndex
        item["equipped"] = character_items[index].equipped

    context = {"inventory_size": character.inventory_size, "items": item_data}

    return render(request, "MUD/inventory.html", context)


@login_required
def update_item(request):
    """
    Updates an items position. Returns 200 or 404

    """
    character = get_character(request.user.username)
    if not character:
        return redirect(reverse("view_character"))

    if request.method == "POST":
        new_item_data = json.load(request)["item_data"]

        itemsettings = ItemSettings.objects.get(
            item__name=new_item_data["name"], character_id=character.id
        )

        if new_item_data["update"] == "both":
            if itemsettings:
                itemsettings.currentSpaceIndex = new_item_data[
                    "currentSpaceIndex"
                ]
                itemsettings.lastSpaceIndex = new_item_data["lastSpaceIndex"]
                itemsettings.equipped = new_item_data["equipped"]
                itemsettings.save()
                return HttpResponse(200)
        elif new_item_data["update"] == "location":
            if itemsettings:
                itemsettings.currentSpaceIndex = new_item_data[
                    "currentSpaceIndex"
                ]
                itemsettings.lastSpaceIndex = new_item_data["lastSpaceIndex"]
                itemsettings.save()
                return HttpResponse(200)
        else:
            if itemsettings:
                print(new_item_data["equipped"])
                itemsettings.equipped = new_item_data["equipped"]
                itemsettings.save()
                return HttpResponse(200)

        return HttpResponse(404)
    else:
        return redirect(reverse("manage_inventory"))
