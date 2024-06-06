<?php
/*
Template Name: All Posts with Images and Categories
*/

get_header();
?>

<div class="category-tabs">
    <?php
    $categories = get_categories();
    if ($categories) :
        foreach ($categories as $category) :
            ?>
            <button class="category-tab" data-category-id="<?php echo esc_attr($category->term_id); ?>">
                <?php echo esc_html($category->name); ?>
            </button>
            <?php
        endforeach;
    endif;
    ?>
</div>

<div class="all-posts-container">
    <?php
    $args = array(
        'post_type' => 'post',
        'posts_per_page' => -1
    );

    $query = new WP_Query($args);

    if ($query->have_posts()) :
        while ($query->have_posts()) : $query->the_post();
            $post_thumbnail = get_the_post_thumbnail_url();
            $post_title = get_the_title();
            $post_link = get_permalink();
            $post_categories = get_the_category();
            $category_classes = '';
            if ($post_categories) {
                foreach ($post_categories as $category) {
                    $category_classes .= ' category-' . $category->term_id;
                }
            }
            ?>
            <div class="post-item<?php echo esc_attr($category_classes); ?>">
                <a href="<?php echo esc_url($post_link); ?>">
                    <div class="post-image" style="background-image: url('<?php echo esc_url($post_thumbnail); ?>');">
                        <div class="post-title-overlay">
                            <h2><?php echo esc_html($post_title); ?></h2>
                        </div>
                    </div>
                </a>
            </div>
            <?php
        endwhile;
        wp_reset_postdata();
    else :
        ?>
        <p><?php esc_html_e('No posts found.'); ?></p>
    <?php endif; ?>
</div>

<?php
get_footer();
?>
