var Cookies = function () { }
Cookies.get = function (key) {
    var cookies = document.cookie;
    var cookiesArray = cookies.split('; ');
    for (var c of cookiesArray) {
        var cArray = c.split('=');
        if (cArray[0] == key) {
            return cArray[1];
        }
    }
    return undefined;
}
Cookies.set = function (key, value, attributes) {
    var attrArray = new Array;
    if (attributes != undefined) {
        Object.keys(attributes).forEach(function (k) {
            attrArray.push(k + "=" + attributes[k]);
        })
    }
    var strKeyValue = key + '=' + value;
    if (attrArray.length != 0) {
        strKeyValue += "; " + attrArray.join("; ");
    }
    document.cookie = strKeyValue;
    return value;
}
Cookies.delete = function (key) {
    var cookies = document.cookie;
    var cookiesArray = cookies.split('; ');
    for (var c of cookiesArray) {
        var cArray = c.split('=');
        if (cArray[0] == key) {
            document.cookie = cArray[0] + '=;max-age=0'
        }
    }
    return undefined;
}
Cookies.reset = function (path) {
    Cookies.keys().forEach(function (k) {
        Cookies.delete(k);
    })
}
Cookies.has = function (key) {
    return (Cookies.get(key) != undefined);
}
Cookies.append = function (key, value, attributes) {
    if (Cookies.has(key)) {
        return Cookies.set(key, Cookies.get(key) + "&|&" + value, attributes);
    } else {
        return Cookies.set(key, value, attributes);
    }
}
Cookies.remove = function (key, value, attributes) {
    if (Cookies.has(key)) {
        var removed = new Array;
        Cookies.getList(key).forEach(function (v) {
            if (v != value) {
                removed.push(v);
            }
        })
        Cookies.set(key, removed.join("&|&"), attributes);
    }
}
Cookies.contain = function (key, value) {
    if (Cookies.has(key)) {
        var contained = false;
        Cookies.getList(key).forEach(function (v) {
            if (v == value) {
                contained = true;
            }
        })
        return contained;
    }
    return false;
}
Cookies.getList = function (key) {
    if (Cookies.has(key)) {
        return Cookies.get(key).split("&|&");
    }
    return [];
}
Cookies.fromJson = function (object, attributes) {
    Object.keys(object).forEach(function (k) {
        Cookies.set(k, object[k], attributes);
    })
}
Cookies.fromJsonString = function (string, attributes) {
    Cookies.fromJson(JSON.parse(string), attributes);
}
Cookies.asJsonString = function () {
    return JSON.stringify(Cookies.asJson());
}
Cookies.asJson = function () {
    var obj = {};
    Cookies.keys().forEach(function (k) {
        obj[k] = Cookies.get(k);
    })
    return obj;
}
Cookies.keys = function () {
    var keys = new Array;
    var cookies = document.cookie;
    var cookiesArray = cookies.split('; ');
    for (var c of cookiesArray) {
        var cArray = c.split('=');
        keys.push(cArray[0]);
    }
    return keys;
}
Cookies.values = function () {
    var values = new Array;
    var cookies = document.cookie;
    var cookiesArray = cookies.split('; ');
    for (var c of cookiesArray) {
        var cArray = c.split('=');
        values.push(cArray[1]);
    }
    return values;
}
