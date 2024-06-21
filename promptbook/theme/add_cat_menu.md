To display a category menu on the top navigation bar in WordPress, you can follow these steps. 

### Step 1: Register a Custom Navigation Menu

First, you'll need to register a custom navigation menu in your theme's `functions.php` file. This allows you to manage the menu via the WordPress admin panel.

```php
function register_my_menu() {
    register_nav_menu('top-navigation', __('Top Navigation'));
}
add_action('init', 'register_my_menu');
```

### Step 2: Add the Categories to the Navigation Menu

Next, you'll need to modify your theme's header file (`header.php`) to include the navigation menu and dynamically populate it with the categories that have no parent (`category_parent == 0`).

```php
<?php
// Get categories with no parent
$args = array(
    'parent'     => 0,
    'orderby'    => 'name',
    'order'      => 'ASC',
    'hide_empty' => false,
);
$categories = get_categories($args);
?>

<nav class="top-navigation">
    <ul>
        <?php foreach ($categories as $category): ?>
            <li>
                <a href="<?php echo get_category_link($category->term_id); ?>">
                    <?php echo esc_html($category->name); ?>
                </a>
            </li>
        <?php endforeach; ?>
    </ul>
</nav>
```

### Step 3: Style the Navigation Menu

To ensure the navigation menu looks good, you'll want to add some CSS. You can do this in your theme's `style.css` file or wherever you manage your theme's styles.

```css
.top-navigation {
    background: #333;
    color: #fff;
}

.top-navigation ul {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
}

.top-navigation ul li {
    margin: 0 10px;
}

.top-navigation ul li a {
    color: #fff;
    text-decoration: none;
    padding: 10px;
    display: block;
}

.top-navigation ul li a:hover {
    background: #444;
}
```

### Step 4: Optional - Manage Menu from Admin Panel

If you want to manage the top navigation menu from the WordPress admin panel, you can use the custom navigation menu registered in Step 1. 

Add the following code to your `header.php`:

```php
<?php
wp_nav_menu(array(
    'theme_location' => 'top-navigation',
    'container'      => 'nav',
    'container_class'=> 'top-navigation',
    'menu_class'     => 'top-navigation-menu',
));
?>
```

And ensure you go to the WordPress admin panel to create and manage the 'Top Navigation' menu under Appearance > Menus.

### Complete Example in `header.php`

Here’s how it all comes together:

```php
<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo('charset'); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
    <header>
        <?php
        wp_nav_menu(array(
            'theme_location' => 'top-navigation',
            'container'      => 'nav',
            'container_class'=> 'top-navigation',
            'menu_class'     => 'top-navigation-menu',
        ));
        ?>

        <!-- Fallback for categories with no parent if menu is not set in admin -->
        <?php
        if (!has_nav_menu('top-navigation')) {
            $args = array(
                'parent'     => 0,
                'orderby'    => 'name',
                'order'      => 'ASC',
                'hide_empty' => false,
            );
            $categories = get_categories($args);
            ?>
            <nav class="top-navigation">
                <ul>
                    <?php foreach ($categories as $category): ?>
                        <li>
                            <a href="<?php echo get_category_link($category->term_id); ?>">
                                <?php echo esc_html($category->name); ?>
                            </a>
                        </li>
                    <?php endforeach; ?>
                </ul>
            </nav>
            <?php
        }
        ?>
    </header>
    <!-- Rest of your theme code -->
</body>
</html>
```

This code provides a fallback if the custom navigation menu is not set in the WordPress admin panel, ensuring that the categories are always displayed.


    [14] => WP_Term Object
        (
            [term_id] => 32
            [name] => Art Types
            [slug] => art-types
            [term_group] => 0
            [term_taxonomy_id] => 32
            [taxonomy] => category
            [description] => Various styles and genres of art
            [parent] => 0
            [count] => 0
            [filter] => raw
            [cat_ID] => 32
            [category_count] => 0
            [category_description] => Various styles and genres of art
            [cat_name] => Art Types
            [category_nicename] => art-types
            [category_parent] => 0
        )