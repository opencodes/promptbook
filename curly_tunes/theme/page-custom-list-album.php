<style>
    .ct-container{
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

    .ct-section .ct-list .ct-item:hover {
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

    .ct-section .ct-list .ct-item:hover .play .fa {
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
        font-size: 12px;
        line-height: 20px;
        font-weight: 600;
    }

    .ct-section hr {
        margin: 70px 0px 0px;
        border-color: #636363;
    }
</style>
<?php
/*
Template Name: Custom Page Album
*/

get_header();
?>
<div class="ct-container">
    <?php
   
            $args = array(
                'post_type' => 'sr_playlist',
                'tax_query' => array(
                    array(
                        'taxonomy' => 'playlist-category',
                        'field' => 'slug',
                        'terms' => 'trending-songs',
                    ),
                ),
            );

            $query = new WP_Query($args);

            if ($query->have_posts()):
                ?>
                <div class="ct-section" id="ct-playlist-<?php echo esc_attr($category->term_id); ?>">
                    <h2>All</h2>
                    <div class="ct-list">
                        <?php
                        while ($query->have_posts()):
                            $query->the_post();
                            $post_thumbnail = get_the_post_thumbnail_url();
                            $post_title = get_the_title();
                            $post_link = get_permalink();
                            $post_categories = get_the_category();
                            $category_classes = '';
                            if ($post_categories) {
                                foreach ($post_categories as $post_category) {
                                    $category_classes .= ' ct-category-' . $post_category->term_id;
                                }
                            }
                            ?>
                            
                                <div class="ct-item<?php echo esc_attr($category_classes); ?>">
                                    <a href="<?php echo esc_url($post_link); ?>"><img src="<?php echo esc_url($post_thumbnail); ?>" />
                                    <div class="play">
                                        <span class="fa fa-play"></span>
                                    </div>
                                    <h4><?php echo esc_html($post_title); ?></h4>
                                    <p>Rema & Selena Gomez are on top of the...</p>
                                    </a>
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
    ?>
</div>

<?php
get_footer();
?>