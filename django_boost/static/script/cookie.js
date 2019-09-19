var Cookies = function(){}
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
Cookies.has = function(key){
    return (Cookies.get(key) != undefined);
}
