<?php
/**
 * Practice theme: presentation only. No business data lives here.
 */

add_action( 'wp_enqueue_scripts', function () {
	wp_enqueue_style( 'practice', get_theme_file_uri( 'assets/practice.css' ), array(), wp_get_theme()->get( 'Version' ) );
} );
add_action( 'after_setup_theme', function () {
	add_editor_style( 'assets/practice.css' );
} );

add_action( 'init', function () {
	register_block_style( 'core/image', array( 'name' => 'leaf', 'label' => __( 'Leaf frame', 'practice' ) ) );
	register_block_style( 'core/group', array( 'name' => 'card', 'label' => __( 'Card', 'practice' ) ) );
	register_block_pattern_category( 'practice', array( 'label' => __( 'Practice', 'practice' ) ) );
	register_block_pattern_category( 'practice-intake', array( 'label' => __( 'Intake status versions', 'practice' ) ) );
} );

/**
 * Pattern helper: markup that places a synced pattern (wp_block) by its slug,
 * so theme patterns can reuse shared business blocks without hard-coded IDs.
 */
function practice_synced( $slug ) {
	$post = get_page_by_path( $slug, OBJECT, 'wp_block' );
	if ( ! $post ) {
		return '<!-- wp:paragraph --><p>[Shared block “' . esc_html( $slug ) . '” not found. Run the setup script.]</p><!-- /wp:paragraph -->';
	}
	return '<!-- wp:block {"ref":' . (int) $post->ID . '} /-->';
}
