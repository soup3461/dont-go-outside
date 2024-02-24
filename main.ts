namespace SpriteKind {
    export const npc = SpriteKind.create()
}

//  variables
let time = 0
let supplies = false
let pot_items = ["food", "water", "battery", "cloth", "wood"]
let needed_items = [""]
needed_items.pop()
let supplies_delivered = 0
let list_len = 0
//  setup
// JESUS CHRIST THIS SHOULD BE NOT THIS
game.showLongText("The world has seen better days... We can't even stay out for long until \"They\" find us. It's your job to get supplies, Press B/ENTER to check your list, then talk to John in your house for the next task!", DialogLayout.Full)
scene.setBackgroundColor(6)
let hero = sprites.create(assets.image`HERO`, SpriteKind.Player)
let john = sprites.create(assets.image`john`, SpriteKind.npc)
controller.moveSprite(hero)
tiles.setCurrentTilemap(tilemap`level`)
scene.cameraFollowSprite(hero)
characterAnimations.setCharacterAnimationsEnabled(hero, true)
characterAnimations.loopFrames(hero, assets.animation`DOWN`, 50, characterAnimations.rule(Predicate.MovingDown))
characterAnimations.loopFrames(hero, assets.animation`UP`, 50, characterAnimations.rule(Predicate.MovingUp))
characterAnimations.loopFrames(hero, assets.animation`RIGHT`, 50, characterAnimations.rule(Predicate.MovingRight))
characterAnimations.loopFrames(hero, assets.animation`LEFT`, 50, characterAnimations.rule(Predicate.MovingLeft))
info.startCountdown(60)
tiles.placeOnRandomTile(hero, assets.tile`bwoo`)
tiles.setTileAt(hero.tilemapLocation(), assets.tile`wood`)
tiles.placeOnRandomTile(john, assets.tile`bwoo`)
tiles.setTileAt(john.tilemapLocation(), assets.tile`wood`)
multilights.toggleLighting(true)
multilights.addLightSource(hero, 15)
function item_place() {
    sprites.destroyAllSpritesOfKind(SpriteKind.Food)
    let food = sprites.create(assets.image`food`, SpriteKind.Food)
    sprites.setDataString(food, "type", "food")
    tiles.placeOnRandomTile(food, assets.tile`shrub`)
    tiles.setTileAt(food.tilemapLocation(), assets.tile`grass`)
    let water = sprites.create(assets.image`water`, SpriteKind.Food)
    sprites.setDataString(water, "type", "water")
    tiles.placeOnRandomTile(water, assets.tile`shrub`)
    tiles.setTileAt(water.tilemapLocation(), assets.tile`grass`)
    let battery = sprites.create(assets.image`battery`, SpriteKind.Food)
    sprites.setDataString(battery, "type", "battery")
    tiles.placeOnRandomTile(battery, assets.tile`shrub`)
    tiles.setTileAt(battery.tilemapLocation(), assets.tile`grass`)
    let cloth = sprites.create(assets.image`cloth`, SpriteKind.Food)
    sprites.setDataString(cloth, "type", "cloth")
    tiles.placeOnRandomTile(cloth, assets.tile`shrub`)
    tiles.setTileAt(cloth.tilemapLocation(), assets.tile`grass`)
    let wood = sprites.create(assets.image`wood`, SpriteKind.Food)
    sprites.setDataString(wood, "type", "wood")
    tiles.placeOnRandomTile(wood, assets.tile`shrub`)
    tiles.setTileAt(wood.tilemapLocation(), assets.tile`grass`)
    for (let supply of sprites.allOfKind(SpriteKind.Food)) {
        tiles.setTileAt(supply.tilemapLocation(), assets.tile`shrub`)
        multilights.addLightSource(supply, 10)
    }
}

item_place()
function wanted_list() {
    let item_to_add: string;
    
    list_len = randint(2, 5)
    for (let i = 0; i < list_len; i++) {
        item_to_add = pot_items[randint(0, 4)]
        if (needed_items.indexOf(item_to_add) < 0) {
            needed_items.push(item_to_add)
        }
        
    }
    list_len = needed_items.length
}

wanted_list()
//  game
//  timer code, timer pauses on interiors/safe zones, restarts on exterior
scene.onOverlapTile(SpriteKind.Player, assets.tile`grass`, function exterior() {
    
    effects.blizzard.startScreenEffect()
    if (time <= 0) {
        return
    } else {
        info.startCountdown(time)
        time = 0
        multilights.bandWidthOf(hero, 30)
    }
    
})
function charint(sprite: Sprite, otherSprite: Sprite) {
    
    if (!supplies) {
        story.printCharacterText(`We need supplies, please go get them 
 The supplies we need are: `, "John")
        game.showLongText(needed_items, DialogLayout.Full)
    } else if (supplies) {
        supplies = false
        story.printCharacterText("Thank you so much! We do however still need some supplies...", "John")
        item_place()
        supplies_delivered += list_len
        wanted_list()
        time += 15
        game.showLongText(needed_items, DialogLayout.Full)
    }
    
}

sprites.onOverlap(SpriteKind.Player, SpriteKind.npc, charint)
scene.onOverlapTile(SpriteKind.Player, assets.tile`wood`, function interior(sprite: Sprite, location: tiles.Location) {
    
    effects.blizzard.endScreenEffect()
    if (time > 0) {
        return
    } else {
        time = info.countdown()
        info.stopCountdown()
        multilights.bandWidthOf(hero, 15)
    }
    
})
//  supply overlap function
sprites.onOverlap(SpriteKind.Player, SpriteKind.Food, function supint(player: Sprite, supply: Sprite) {
    
    if (needed_items.indexOf(sprites.readDataString(supply, "type")) >= 0) {
        needed_items.removeAt(needed_items.indexOf(sprites.readDataString(supply, "type")))
        if (needed_items.length == 0) {
            supplies = true
        }
        
    } else {
        info.changeCountdownBy(2)
    }
    
    sprites.destroy(supply)
})
//  we can't always have john to tell us what we need, luckily we have a notepad 
controller.B.onEvent(ControllerButtonEvent.Pressed, function open_list() {
    
    if (needed_items.length > 0) {
        game.showLongText(needed_items, DialogLayout.Full)
    } else {
        game.showLongText("Go Talk to John in the house!", DialogLayout.Full)
    }
    
})
charint(hero, john)
game.onUpdate(function on_update() {
    console.log(time)
    console.log(needed_items)
    console.log(supplies_delivered)
})
//  On timer 0, set supplies delivered to score, game over splash after a little cs!
info.onCountdownEnd(function endgame() {
    
    info.setScore(supplies_delivered)
    game.showLongText("Ah, they found you, you've been outside too long... It's ok though, you managed to deliver: " + info.score() + " supplies to help rebuild the nation! Try again to get even more!", DialogLayout.Full)
    game.gameOver(false)
})
