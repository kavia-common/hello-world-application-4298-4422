from typing import Optional, Dict

from django import template

register = template.Library()

# PUBLIC_INTERFACE
@register.inclusion_tag("components/button.html")
def button(
    button_label: str,
    href: Optional[str] = None,
    variant: str = "primary",
    size: str = "md",
    icon_left: Optional[str] = None,
    icon_right: Optional[str] = None,
    disabled: bool = False,
    loading: bool = False,
    id: Optional[str] = None,
    extra_classes: str = "",
    type: str = "button",
    name: Optional[str] = None,
    value: Optional[str] = None,
    title: Optional[str] = None,
    aria_label: Optional[str] = None,
    # New: full-width / responsive flags
    block: bool = False,
    block_sm: bool = False,
    block_md: bool = False,
    block_lg: bool = False,
) -> Dict:
    """
    Render a reusable, accessible button/anchor with variants, icons, states, and block/responsive utilities.

    Parameters:
    - button_label: Visible text for the button.
    - href: If provided, renders an anchor; otherwise renders a <button>.
    - variant: visual style. Supported: primary, secondary, success, outline, ghost, link.
    - size: size scale. Supported: sm, md, lg.
    - icon_left: optional class name for leading icon (e.g., 'icon icon-mail'). Rendered in a <span>.
    - icon_right: optional class name for trailing icon.
    - disabled: disables the control. For anchors, sets aria-disabled="true" and prevents clicks.
    - loading: shows spinner, sets aria-busy="true", and prevents interaction.
    - id: optional id on the element.
    - extra_classes: additional class names appended to the element.
    - type: button type attribute when rendering <button>. Defaults to "button".
    - name, value: form attributes for <button>.
    - title: optional title attribute.
    - aria_label: optional aria-label attribute. When provided, will be applied.
    - block: when True, make the button full-width (100%).
    - block_sm|block_md|block_lg: responsive full-width at the respective breakpoint.

    Returns:
    A dict context for the 'components/button.html' template.
    """
    # Normalize and validate variant/size
    allowed_variants = {"primary", "secondary", "success", "outline", "ghost", "link"}
    if variant not in allowed_variants:
        variant = "primary"

    allowed_sizes = {"sm", "md", "lg"}
    if size not in allowed_sizes:
        size = "md"

    # Compose classes
    classes = [
        "ui-btn",
        f"ui-btn--{variant}",
        f"ui-btn--{size}",
    ]

    # Block utilities
    if block:
        classes.append("btn-block")
    if block_sm:
        classes.append("sm:btn-block")
    if block_md:
        classes.append("md:btn-block")
    if block_lg:
        classes.append("lg:btn-block")

    if disabled:
        classes.append("is-disabled")
    if loading:
        classes.append("is-loading")
    if extra_classes:
        classes.append(extra_classes.strip())

    attrs = {
        "id": id or "",
        "class": " ".join(classes).strip(),
        "title": title or "",
        "aria_label": aria_label or "",
        "name": name or "",
        "value": value or "",
    }

    # Accessibility attributes
    attrs["aria_disabled"] = "true" if disabled else "false"
    attrs["aria_busy"] = "true" if loading else "false"

    # For a real <button>, we keep the 'type' attribute; for anchor, it's ignored in template.
    attrs["type"] = type

    return {
        "button_label": button_label,
        "href": href,
        "variant": variant,
        "size": size,
        "icon_left": icon_left,
        "icon_right": icon_right,
        "disabled": disabled,
        "loading": loading,
        "attrs": attrs,
    }
