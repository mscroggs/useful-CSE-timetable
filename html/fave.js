var chars = Array(
    "_", "1", "2", "3", "4", "5", "6", "7",
    "8", "9", "A", "B", "C", "D", "E", "F",
    "G", "H", "I", "J", "K", "L", "M", "O",
    "P", "Q", "R", "S", "T", "U", "V", "W",
    "X", "Y", "Z", "a", "b", "c", "d", "e",
    "f", "g", "h", "i", "j", "k", "l", "m",
    "n", "o", "p", "q", "r", "s", "t", "u",
    "v", "w", "x", "y", "z", "!", "?", "-",
)
var nchar = 6
console.assert(Math.pow(2, nchar) == chars.length)

function encode(input_list, short) {
    var output = ""
    for (var i = 0; i < input_list.length; i += nchar) {
        var dec = 0
        for (var j = 0; j < nchar && i + j < input_list.length; j++) {
            if (input_list[i + j] == 1) {
                dec += Math.pow(2, j)
            }
        }
        output += chars[dec]
    }
    while (output.charAt(output.length-1) == "_") {
        output = output.substr(0, output.length - 1)
    }
    if (!short) {
        return output
    }
    output2 = ""
    var n_ = 0
    for (var i = 0; i < output.length; i++) {
        var c = output.charAt(i)
        if (c == "_") {
            n_++
        } else {
            if (n_ > 0) {
                output2 += "_" + n_ + "_"
                n_ = 0
            }
            output2 += c
        }
    }
    if (n_ > 0) {
        output2 += "_" + n_ + "_"
    }
    return output2
}

function decode(input_str, short) {
    if (short) {
        var new_input = ""
        for (var i = 0; i < input_str.length; i++) {
            c = input_str.charAt(i)
            if (c == "_") {
                j = 1
                while (input_str.charAt(i + j + 1) != "_") {
                    j += 1
                }
                var n = input_str.substr(i + 1, j) / 1
                for (var k = 0; k < n; k++) {
                    new_input += "_"
                }
                i += j + 1
            } else {
                new_input += c
            }
        }
        input_str = new_input
    }
    var output = Array()
    for (var i = 0; i < input_str.length; i++) {
        var c = chars.indexOf(input_str.substring(i, i + 1))
        for (var j = 0; j < nchar && output.length < {{order.length}}; j++) {
            output[output.length] = c % 2
            c = (c - output[output.length-1]) / 2
        }
    }
    while (output.length < {{order.length}}) {
        output[output.length] = 0
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
        faves = decode(cookies[i].split("=")[1], false)
    }
}
function update_stars() {
    for (var i = 0; i < {{order.length}}; i++) {
        var e = document.getElementById("talk" + i)
        if (e != null) {
            if (faves[i] == 1) {
                e.style.display = "block"
            } else {
                e.style.display = "none"
            }
        }
    }
    for (var i = 0; i < {{order.length}}; i++) {
        var elements = document.getElementsByClassName("star" + i)
        if (faves[i] == 1) {
            for (var j = 0; j < elements.length; j++) {
                elements[j].innerHTML = "&starf;"
                elements[j].style.color = "gold"
            }
        } else {
            for (var j = 0; j < elements.length; j++) {
                elements[j].innerHTML = "&star;"
                elements[j].style.color = "gray"
            }
        }
    }
}


function toggle_star(n) {
    faves[n] = 1 - faves[n]
    save_stars()
    update_stars()
}

function save_stars() {
    var faves_str = encode(faves, false)
    document.cookie = "faves=" + faves_str + "; expires=Mon, 18 Dec 2023 12:00:00 UTC; path=/"
}

function show_bit(i) {
    document.getElementById("bit-"+i).style.display = "inline"
    document.getElementById("bitlink-"+i).style.display = "none"
}

function hide_bit(i) {
    document.getElementById("bit-"+i).style.display = "none"
    document.getElementById("bitlink-"+i).style.display = "inline"
}
