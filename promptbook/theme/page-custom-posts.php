<?php
/*
Template Name: All Posts with Images and Categories
*/

get_header();
?>
<?php
                $categories = get_categories();
                ?>
                <!-- <pre style="width:500px;"><?php //print_r($categories); ?></pre>  -->
<div class="custom-nav site-bottom-header-wrap site-header-row-container site-header-focus-item site-header-row-layout-standard"
    data-section="kadence_customizer_header_bottom">
    <div class="site-header-row-container-inner">
        <div class="site-container">
            <div class="category-tabs">
                <?php
                if ($categories):
                    foreach ($categories as $category):
                        if ($category->category_parent == 0):
                        ?>
                        <a href="<?php echo get_category_link($category->term_id) ?>" class="category-tab" data-category-id="<?php echo esc_attr($category->term_id); ?>">
                            <?php echo esc_html($category->name); ?>
                        </a>
                        <?php
                        endif;
                    endforeach;
                endif;
                ?>
            </div>
        </div>
    </div>
</div>



<div class="ct-section">
    <div class="ct-list">
        <?php
        $args = array(
            'post_type' => 'post',
            'posts_per_page' => -1
        );

        $query = new WP_Query($args);

        if ($query->have_posts()):
            while ($query->have_posts()):
                $query->the_post();
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
                <div class="post-item <?php echo esc_attr($category_classes); ?>">
                    <a href="<?php echo esc_url($post_link); ?>">
                        <img src="<?php echo esc_url($post_thumbnail); ?>" />
                    </a>
                    <h4><a href="<?php echo esc_url($post_link); ?>"><?php echo esc_html($post_title); ?></a></h4>
                    <p class="tags">
                    <?php foreach ($post_categories as $category): ?>
                    <span><?php echo esc_html($category->name); ?></span>
                    <?php endforeach; ?>
                    </p>
                </div>
                <?php
            endwhile;
            wp_reset_postdata();
        else:
            ?>
            <p><?php esc_html_e('No posts found.'); ?></p>
        <?php endif; ?>
    </div>
</div>

<?php
get_footer();
?>