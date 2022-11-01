interpolate = function (fmt, obj, named) {
	if (named) {
	return fmt.replace(/%\(\w+\)s/g, function(match){return String(obj[match.slice(2,-2)])});
	} else {
	return fmt.replace(/%s/g, function(match){return String(obj.shift())});
	}
};
ngettext = function (singular, plural, count) { return (count == 1) ? singular : plural; };
