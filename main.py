@namespace
class SpriteKind:
    npc = SpriteKind.create()

# variables
time = 0
supplies = False
pot_items = ["food", "water", "battery", "cloth", "wood"]
needed_items = [""]
needed_items.pop()
supplies_delivered = 0
list_len = 0
minimap_open = False
# setup

#JESUS CHRIST THIS SHOULD BE NOT THIS
game.show_long_text("The world has seen better days... We can't even stay out for long until \"They\" find us. It's your job to get supplies, Press B/ENTER to check your list, then talk to John in your house for the next task!", DialogLayout.FULL)
scene.set_background_color(6)
hero = sprites.create(assets.image("HERO"), SpriteKind.player)
john = sprites.create(assets.image("john"), SpriteKind.npc)
controller.move_sprite(hero)
tiles.set_current_tilemap(tilemap("level"))
scene.camera_follow_sprite(hero)
characterAnimations.set_character_animations_enabled(hero, True)
characterAnimations.loop_frames(hero, assets.animation("DOWN"), 50, characterAnimations.rule(Predicate.MOVING_DOWN))
characterAnimations.loop_frames(hero, assets.animation("UP"), 50, characterAnimations.rule(Predicate.MOVING_UP))
characterAnimations.loop_frames(hero, assets.animation("RIGHT"), 50, characterAnimations.rule(Predicate.MOVING_RIGHT))
characterAnimations.loop_frames(hero, assets.animation("LEFT"), 50, characterAnimations.rule(Predicate.MOVING_LEFT))
info.start_countdown(60)
tiles.place_on_random_tile(hero, (assets.tile("bwoo")))
tiles.set_tile_at(hero.tilemap_location(), assets.tile("wood"))
tiles.place_on_random_tile(john, (assets.tile("bwoo")))
tiles.set_tile_at(john.tilemap_location(), assets.tile("wood"))
multilights.toggle_lighting(True)
multilights.add_light_source(hero, 15)
def item_place():
    sprites.destroy_all_sprites_of_kind(SpriteKind.food)
    food = sprites.create(assets.image("food"), SpriteKind.food)
    sprites.set_data_string(food, "type", "food")
    tiles.place_on_random_tile(food, (assets.tile("shrub")))
    tiles.set_tile_at(food.tilemap_location(), assets.tile("grass"))
    water = sprites.create(assets.image("water"), SpriteKind.food)
    sprites.set_data_string(water, "type", "water")
    tiles.place_on_random_tile(water, (assets.tile("shrub")))
    tiles.set_tile_at(water.tilemap_location(), assets.tile("grass"))
    battery = sprites.create(assets.image("battery"), SpriteKind.food)
    sprites.set_data_string(battery, "type", "battery")
    tiles.place_on_random_tile(battery, (assets.tile("shrub")))
    tiles.set_tile_at(battery.tilemap_location(), assets.tile("grass"))
    cloth = sprites.create(assets.image("cloth"), SpriteKind.food)
    sprites.set_data_string(cloth, "type", "cloth")
    tiles.place_on_random_tile(cloth, (assets.tile("shrub")))
    tiles.set_tile_at(cloth.tilemap_location(), assets.tile("grass"))
    wood = sprites.create(assets.image("wood"), SpriteKind.food)
    sprites.set_data_string(wood, "type", "wood")
    tiles.place_on_random_tile(wood, (assets.tile("shrub")))
    tiles.set_tile_at(wood.tilemap_location(), assets.tile("grass"))
    for supply in sprites.all_of_kind(SpriteKind.food):
        tiles.set_tile_at(supply.tilemap_location(), assets.tile("shrub"))
        multilights.add_light_source(supply, 10)

item_place()
def wanted_list():
    global pot_items, needed_items, list_len
    list_len = randint(2,5)
    for i in range (list_len):
        item_to_add = pot_items[randint(0,4)]
        if item_to_add not in needed_items:
            needed_items.append(item_to_add)
    list_len = len(needed_items)
        
wanted_list()

# game

# timer code, timer pauses on interiors/safe zones, restarts on exterior
def exterior():
    global time
    effects.blizzard.start_screen_effect()
    if time <= 0:
        return
    else:
        info.start_countdown(time)
        time = 0
        multilights.band_width_of(hero, 30)
scene.on_overlap_tile(SpriteKind.player, assets.tile("grass"), exterior)
def interior(sprite, location):
    global time
    effects.blizzard.end_screen_effect()
    if time > 0:
        return 
    else:
        time = info.countdown()
        info.stop_countdown()
        multilights.band_width_of(hero, 15)

def charint(sprite, otherSprite):
    global supplies, needed_items, time, list_len, supplies_delivered
    if not supplies:
        story.print_character_text("We need supplies, please go get them \n The supplies we need are: ", "John")
        game.show_long_text(needed_items, DialogLayout.FULL)
    elif supplies:
        supplies = False
        story.print_character_text("Thank you so much! We do however still need some supplies...", "John")
        item_place()
        supplies_delivered += list_len
        wanted_list()
        time += 15
        game.show_long_text(needed_items, DialogLayout.FULL)
sprites.on_overlap(SpriteKind.player, SpriteKind.npc, charint)

scene.on_overlap_tile(SpriteKind.player, assets.tile("wood"), interior)
# supply overlap function
def supint(player, supply):
    global supplies, needed_items, time
    if sprites.read_data_string(supply, "type") in needed_items:
        needed_items.remove_at(needed_items.index(sprites.read_data_string(supply, "type") ))
        if len(needed_items) == 0:
            supplies = True
    else:
        if time == 0:
            info.change_countdown_by(4) #it's 4 now, thank Emi
        else:
            time += 4
    sprites.destroy(supply)
sprites.on_overlap(SpriteKind.player, SpriteKind.food, supint)

# we can't always have john to tell us what we need, luckily we have a notepad 
def open_list():
    global needed_items
    if len(needed_items) > 0:
        game.show_long_text(needed_items, DialogLayout.FULL)
    else:
        game.show_long_text("Go Talk to John in the house!", DialogLayout.FULL)
controller.B.on_event(ControllerButtonEvent.PRESSED, open_list)
charint(hero, john)

def on_update():
    console.log(time)
    console.log(needed_items) 
    console.log(supplies_delivered)
game.on_update(on_update)

# On timer 0, set supplies delivered to score, game over splash after a little cs!
def endgame():
    global supplies_delivered
    info.set_score(supplies_delivered)
    game.show_long_text("Ah, they found you, you've been outside too long... It's ok though, you managed to deliver: " + info.score() + " supplies to help rebuild the nation! Try again to get even more!" , DialogLayout.FULL)
    game.game_over(False)
info.on_countdown_end(endgame)

#minimap, might be useful for some people
minimap_object = minimap.minimap(MinimapScale.EIGHTH, 2, 15)
minimap_image = minimap.get_image(minimap_object)
minimap_sprite = sprites.create(minimap_image)
minimap_sprite.z = 100
minimap_sprite.set_flag(SpriteFlag.RELATIVE_TO_CAMERA, True)
minimap_sprite.set_flag(SpriteFlag.INVISIBLE, True)
# on menu because I hate everyone ig
def toggle_map():
    global minimap_open
    if minimap_open:
        minimap_sprite.set_flag(SpriteFlag.INVISIBLE, True)
        minimap_open = False
    else:
        minimap_sprite.set_flag(SpriteFlag.INVISIBLE, False)
        minimap_open = True
controller.menu.on_event(ControllerButtonEvent.PRESSED, toggle_map)

def update_minimap():
    if minimap_open:
        minimap_object = minimap.minimap(MinimapScale.EIGHTH, 2, 15)
        minimap.include_sprite(minimap_object, hero, MinimapSpriteScale.QUADRUPLE)
        for supply in sprites.all_of_kind(SpriteKind.food):
            minimap.include_sprite(minimap_object, supply, MinimapSpriteScale.OCTUPLE)
        minimap_sprite.set_image(minimap.get_image(minimap_object))
game.on_update_interval(100, update_minimap)