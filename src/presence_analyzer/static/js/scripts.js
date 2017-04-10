function parseInterval(value) {
    var result = new Date(1, 1, 1);
    result.setMilliseconds(value * 1000);
    return result;
}

function parseToDate(value) {
    var result = new Date(value);
    return result
}
