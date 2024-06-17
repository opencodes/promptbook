<style>
    .ct-container {
        width: 100%;
    }
    .ct-section {
        padding: 20px 40px;
    }
    .ct-section h2 {
        font-size: 22px;
        margin-bottom: 20px;
    }
    .ct-section .ct-list {
        display: flex;
        gap: 20px;
        overflow: hidden;
    }
    .ct-section .ct-list .ct-item {
        min-width: 140px;
        max-width: 200px;
        padding: 15px;
        border-radius: 6px;
        cursor: pointer;
        transition: all ease 0.4s;
    }
    .ct-section .ct-list .ct-item a:hover{
        text-decoration: underline;
    }
    .ct-section .ct-list .ct-item:hover {
        background-color: #f2f2f2;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
    }
    .ct-section .ct-list .ct-item img:hover {
        opacity: 0.8;
    }
    .ct-section .ct-list .ct-item img {
        width: 100%;
        border-radius: 6px;
        margin-bottom: 10px;
    }
    .ct-section .ct-list .ct-item .play {
        position: relative;
    }
    .ct-section .ct-list .ct-item .play .fa {
        position: absolute;
        right: 10px;
        top: -60px;
        padding: 18px;
        background-color: #1db954;
        border-radius: 100%;
        opacity: 0;
        transition: all ease 0.4s;
    }
    .ct-section .ct-list .ct-item img:hover .play .fa {
        opacity: 1;
        transform: translateY(-20px);
    }
    .ct-section .ct-list .ct-item h4 {
        font-size: 14px;
        margin-bottom: 10px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .ct-section .ct-list .ct-item p {
        font-size: 10px;
        line-height: 12px;
        margin: 0;
        font-weight: 500;
        padding-bottom: 5px;
    }
    .ct-section hr {
        margin: 70px 0px 0px;
        border-color: #636363;
    }
</style>
<?php
/*
Template Name: Custom Page Dashboard
*/

get_header();
?>
<div class="ct-container">
    <?php
    $args = array(
        'taxonomy' => 'playlist-category',
    );
    $categories = get_categories($args);
    if ($categories):
        foreach ($categories as $category):
            $args = array(
                'post_type' => 'sr_playlist',
                'posts_per_page' => 10,
                'tax_query' => array(
                    array(
                        'taxonomy' => 'playlist-category',
                        'field' => 'term_id',
                        'terms' => $category->term_id,
                    ),
                ),
            );

            $query = new WP_Query($args);

            if ($query->have_posts()):
                ?>
                <div class="ct-section" id="ct-playlist-<?php echo esc_attr($category->term_id); ?>">
                    <h2><?php echo esc_html($category->name); ?></h2>
                    <div class="ct-list">
                        <?php
                        while ($query->have_posts()):
                            $query->the_post();
                            $post_id = get_the_ID();
                            $post_data = array(
                                'ID' => $post_id,
                                'title' => get_the_title(),
                                'excerpt' => get_the_excerpt(),
                                'thumbnail' => get_the_post_thumbnail_url() ?: 'default-image-url.jpg', // Provide a default image URL
                                'link' => get_permalink(),
                                'categories' => get_the_terms($post_id, 'playlist-category'),
                                'tags' => get_the_terms($post_id, 'playlist-tag'),
                            );

                            $category_names = $post_data['categories'] ? wp_list_pluck($post_data['categories'], 'name') : array();
                            $tag_names = $post_data['tags'] ? wp_list_pluck($post_data['tags'], 'name') : array();
                            ?>
                            <div class="ct-item">
                                    <a href="<?php echo esc_url($post_data['link']); ?>">
                                        <img src="<?php echo esc_url($post_data['thumbnail']); ?>" alt="<?php echo esc_attr($post_data['title']); ?>" />
                                    </a>
                                    <div class="play">
                                        <a href="<?php echo esc_url($post_data['link']); ?>"><span class="fa fa-play"></span></a>
                                    </div>
                                    <h4><a href="<?php echo esc_url($post_data['link']); ?>"><?php echo esc_html($post_data['title']); ?></a></h4>
                                    <p><?php echo esc_html($post_data['excerpt']); ?></p>
                                    <p class="categories"><?php echo esc_html(implode('  ', $category_names)); ?></p>
                                    <p class="tags"><?php echo esc_html(implode('  ', $tag_names)); ?></p>
                                
                            </div>
                        <?php
                        endwhile;
                        ?>
                    </div>
                </div>
                <?php
                wp_reset_postdata();
            else:
                ?>
                <p><?php esc_html_e('No posts found in this category.'); ?></p>
                <?php
            endif;
        endforeach;
    endif;
    ?>
</div>

<?php
get_footer();
?>
