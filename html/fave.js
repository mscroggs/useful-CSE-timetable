var chars = Array(
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
    "K", "L", "M", "O", "P", "Q", "R", "S", "T", "U",
    "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e",
    "f", "g", "h", "i", "j", "k", "l", "m", "n", "o",
    "p", "q", "r", "s", "t", "u", "v", "w", "x", "y",
    "z"
)

function encode(data) {
    var output = ""
    for (var i = 0; i < data.length; i++) {
        output += data[i]
        if (i < data.length - 1) {
            output += "a"
        }
    }
    return output
}

function decode(data) {
    var output = Array()
    for (var i = 0; i < {{order.length}}; i++) {
        output[output.length] = 0
    }
    for (var j = 0; j < data.length; j++) {
        output[j] = data[j]
    }
    return output
}

var faves = Array()
for (var i = 0; i < {{order.length}}; i++) {
    faves[faves.length] = 0
}
var cookies = document.cookie.split(";")
for (var i = 0; i < cookies.length; i++) {
    if (cookies[i].split("=")[0].trim() == "faves") {
        faves = decode(cookies[i].split("=")[1].split("a"))
    }
}


function update_stars() {
    for (var i = 0; i < {{order.length}}; i++) {
        var elements = document.getElementsByClassName("star" + i)
        if (faves[i] == 1) {
            var e = document.getElementById("talk" + i)
            if (e != null) {
                e.style.display = "block"
            }
            for (var j = 0; j < elements.length; j++) {
                elements[j].innerHTML = "&starf;"
                elements[j].style.color = "gold"
            }
        } else {
            var e = document.getElementById("talk" + i)
            if (e != null) {
                e.style.display = "none"
            }
            for (var j = 0; j < elements.length; j++) {
                elements[j].innerHTML = "&star;"
                elements[j].style.color = "gray"
            }
        }
    }
}


function toggle_star(n) {
    faves[n] = 1 - faves[n]

    var faves_str = encode(faves)
    document.cookie = "faves=" + faves_str + "; expires=Mon, 18 Dec 2023 12:00:00 UTC; path=/"
    update_stars()
}
