from django import template
from django.utils.safestring import mark_safe

from usom.views import admin_menus

register = template.Library()


@register.simple_tag
def get_menus(user=None, path=None):
    menus = ""
    menu_list = admin_menus(user)
    for item in menu_list:
        if item.get("header", None):
            menus += """
            <li class="menu-section">
                <h4 class="menu-text">{}</h4>
                <i class="menu-icon ki ki-bold-more-hor icon-md"></i>
            </li>
            """.format(
                item["title"]
            )
        else:
            children = item.get("children", None)
            if children:
                is_active = False
                for child in item["children"]:
                    if child.get("url", "#") == path:
                        is_active = True
                menus += """
                <li
                class="menu-item menu-item-submenu {}"
                aria-haspopup="true"
                data-menu-toggle="hover">
                    <a href="javascript:;" class="menu-link menu-toggle">
                        <span class="menu-icon">
                            <i class="{}"></i>
                        </span>
                        <span class="menu-text">{}</span>
                        <i class="menu-arrow"></i>
                    </a>
                    <div class="menu-submenu">
                        <i class="menu-arrow"></i>
                        <ul class="menu-subnav">
                            <li class="menu-item menu-item-parent" aria-haspopup="true">
                                <span class="menu-link">
                                    <span class="menu-text">{}</span>
                                </span>
                            </li>
                """.format(
                    "menu-item-open menu-item-here" if is_active else "",
                    item["icon"],
                    item["title"],
                    item["title"],
                )

                for child in item["children"]:
                    is_active_child = child["url"] == path
                    menus += """
                    <li
                    class="menu-item {}"
                    data-menu-toggle="hover"
                    aria-haspopup="true">
                        <a href="{}" class="menu-link">
                            <span class="menu-icon">
                                <i class="{}"> </i>
                            </span>
                            <span class="menu-text">{}</span>
                        </a>
                    </li>
                    """.format(
                        "menu-item-active" if is_active_child else "",
                        child.get("url", "#"),
                        child.get("icon", ""),
                        child.get("title", ""),
                    )
                menus += """
                        </ul>
                    </div>
                </li>
                """
            else:
                is_active = item["url"] == path
                menus += """
                <li class="menu-item {}" aria-haspopup="true">
                    <a href="{}" class="menu-link">
                        <i class="menu-icon {}"></i>
                        <span class="menu-text">{}</span>
                    </a>
                </li>
                """.format(
                    "menu-item-active" if is_active else "",
                    item["url"],
                    item["icon"],
                    item["title"],
                )
    return mark_safe(menus)
