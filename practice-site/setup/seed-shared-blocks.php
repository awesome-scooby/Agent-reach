<?php
/**
 * Step 1 of 2: create the shared business blocks (synced patterns) and site settings.
 *
 * Placeholder data only. No real fees, names, credentials or clinical content.
 * Safe to run more than once: existing records are left untouched.
 *
 * Run on a staging site with:  wp eval-file seed-shared-blocks.php
 */

if ( ! defined( 'ABSPATH' ) ) {
	require_once '/wordpress/wp-load.php';
}

function practice_seed_block( $slug, $title, $content ) {
	$existing = get_page_by_path( $slug, OBJECT, 'wp_block' );
	if ( $existing ) {
		return $existing->ID;
	}
	return wp_insert_post( wp_slash( array(
		'post_type'    => 'wp_block',
		'post_status'  => 'publish',
		'post_name'    => $slug,
		'post_title'   => $title,
		'post_content' => $content,
	) ) );
}

function practice_fee_markup( $label, $amount, $note ) {
	return '<!-- wp:group {"className":"practice-fee","layout":{"type":"default"}} -->
<div class="wp-block-group practice-fee"><!-- wp:paragraph --><p><strong>' . $label . '</strong></p><!-- /wp:paragraph -->
<!-- wp:paragraph {"className":"practice-fee__amount"} --><p class="practice-fee__amount">' . $amount . '</p><!-- /wp:paragraph -->
<!-- wp:paragraph {"fontSize":"small","textColor":"muted","style":{"layout":{"selfStretch":"fill"}}} --><p class="has-muted-color has-text-color has-small-font-size">' . $note . '</p><!-- /wp:paragraph --></div>
<!-- /wp:group -->';
}

// Fees: one shared block per fee. Edit the amount here once; every page updates.
practice_seed_block( 'fee-standard-session', 'Fee – Standard session',
	practice_fee_markup( 'Standard session · [50] minutes', '$[fee]', 'Fee from [date]. <span class="practice-draft">draft, not approved</span>' ) );
practice_seed_block( 'fee-extended-session', 'Fee – Extended session',
	practice_fee_markup( 'Extended session · [80] minutes', '$[fee]', 'If offered. <span class="practice-draft">draft, not approved</span>' ) );

// Booking action starts in the "open" state, using the theme's ready-made version.
ob_start();
include get_theme_file_path( 'patterns/booking-open.php' );
$open = trim( preg_replace( '#^.*?\?>#s', '', ob_get_clean() ) );
practice_seed_block( 'booking-action', 'Booking action (intake status)', $open );

practice_seed_block( 'contact-details', 'Contact details', '<!-- wp:paragraph -->
<p>Telehealth across [Australia]. No consulting room yet. <span class="practice-draft">confirm</span></p>
<!-- /wp:paragraph -->
<!-- wp:paragraph -->
<p>Phone: [0000 000 000]<br>Email: [admin@example.invalid]<br>Hours: [Mon–Thu, 9am–5pm] AWST (Perth time)</p>
<!-- /wp:paragraph -->
<!-- wp:paragraph {"fontSize":"small"} -->
<p class="has-small-font-size">Messages are checked during business hours only.</p>
<!-- /wp:paragraph -->' );

practice_seed_block( 'urgent-help', 'Urgent help', '<!-- wp:heading {"level":2,"fontSize":"large"} -->
<h2 class="wp-block-heading has-large-font-size">Need urgent help?</h2>
<!-- /wp:heading -->
<!-- wp:paragraph -->
<p>If you or someone else is in danger, call 000. For crisis support at any time, call Lifeline on 13 11 14. This practice can\'t respond to urgent messages. <span class="practice-draft">wording to verify before launch</span></p>
<!-- /wp:paragraph -->' );

// Staging safety and locale.
update_option( 'blog_public', 0 );             // Discourage search engines on staging.
update_option( 'blogname', 'Practice name' );
update_option( 'blogdescription', '' );
update_option( 'timezone_string', 'Australia/Perth' );
update_option( 'date_format', 'j F Y' );
update_option( 'WPLANG', '' );
update_option( 'permalink_structure', '/%postname%/' );
flush_rewrite_rules();

echo "Shared blocks ready.\n";
