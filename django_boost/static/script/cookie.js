var Cookies = () => document.cookie;
Cookies.get = (key) => {
    const item = Cookies.entries().filter(i => i[0] === key);
    return !!item.length ? item[0][1] : undefined;
}
Cookies.set = (key, value, attributes) => {
    var strKeyValue = key + '=' + value;
    if (attributes !== undefined) {
        strKeyValue += "; " + Object.entries(attributes).map(k => k[0] + "=" + k[1]).join("; ");
    }
    document.cookie = strKeyValue;
    return value;
}
Cookies.delete = (key) => {
    for (var k of Cookies.keys().filter(k => k=== key)) {
        document.cookie = k + '=;max-age=0';
    }
    return undefined;
}
Cookies.reset = (path) => { Cookies.keys().forEach(k => Cookies.delete(k)) };

Cookies.has = (key) => !!Cookies.keys().filter(i => i === key).length

Cookies.append = (key, value, attributes) => Cookies.set(key, [...Cookies.getList(key), value].join("&|&"), attributes)

Cookies.remove = (key, value, attributes) => {
    if (Cookies.has(key)) {
        var removed = Cookies.getList(key).filter(v => v !== value);
        Cookies.set(key, removed.join("&|&"), attributes);
    }
}
Cookies.contain = (key, value) => !!Cookies.getList(key).filter(v => v === value).length

Cookies.getList = (key) => Cookies.has(key) ? Cookies.get(key).split("&|&") : [];

Cookies.fromJson = (object, attributes) => Cookies.fromEntries(Object.entries(object).map(v => [...v, attributes]))

Cookies.fromJsonString = (string, attributes) => Cookies.fromJson(JSON.parse(string), attributes);

Cookies.asJsonString = () => JSON.stringify(Cookies.asJson());

Cookies.asJson = () => Object.fromEntries(Cookies.entries());

Cookies.items = () => Cookies().split('; ').filter(v => v !== "");

Cookies.entries = () => Cookies.items().map(i => i.split("="));

Cookies.fromEntries = (entries) => entries.forEach(entry => Cookies.set(entry[0], entry[1], entry[2]))

Cookies.keys = () => Cookies.entries().map(i => i[0]);

Cookies.values = () => Cookies.entries().map(i => i[1]);
