<?php
/**
 * Step 2 of 2: create pages from the theme's patterns, the menu and the front page.
 *
 * Patterns are expanded into real blocks and saved as page content, so pages
 * belong to the database (and survive a redesign), not to the theme.
 * Placeholder data only. Safe to re-run: existing pages are left untouched.
 */

if ( ! defined( 'ABSPATH' ) ) {
	require_once '/wordpress/wp-load.php';
}

function practice_pattern( $slug ) {
	$p = WP_Block_Patterns_Registry::get_instance()->get_registered( 'practice/' . $slug );
	return $p ? $p['content'] : '';
}

function practice_page( $slug, $title, $content, $args = array() ) {
	$existing = get_page_by_path( isset( $args['path'] ) ? $args['path'] : $slug );
	if ( $existing ) {
		return $existing->ID;
	}
	$id = wp_insert_post( wp_slash( array_merge( array(
		'post_type'    => 'page',
		'post_status'  => 'publish',
		'post_name'    => $slug,
		'post_title'   => $title,
		'post_content' => $content,
	), array_diff_key( $args, array( 'path' => 1, 'template' => 1 ) ) ) ) );
	if ( ! empty( $args['template'] ) ) {
		update_post_meta( $id, '_wp_page_template', $args['template'] );
	}
	return $id;
}

function practice_stub( $what ) {
	return '<!-- wp:paragraph --><p>' . $what . ' <span class="practice-draft">stage 3</span></p><!-- /wp:paragraph -->';
}

function practice_ref( $slug ) {
	return practice_synced( $slug );
}

$home = practice_page( 'home', 'Home', implode( "\n\n", array(
	practice_pattern( 'hero' ),
	practice_pattern( 'is-this-for-you' ),
	practice_pattern( 'practitioner-intro' ),
	practice_pattern( 'service-list' ),
	practice_pattern( 'fee-summary' ),
	practice_pattern( 'what-happens-next' ),
) ), array( 'template' => 'page-no-title' ) );

$fees_content = '<!-- wp:paragraph {"fontSize":"large"} --><p class="has-large-font-size">Here is what a session costs, what happens at your first appointment, and what to do if you need to cancel.</p><!-- /wp:paragraph -->

<!-- wp:heading --><h2 class="wp-block-heading">Session fees</h2><!-- /wp:heading -->
' . practice_ref( 'fee-standard-session' ) . '
' . practice_ref( 'fee-extended-session' ) . '

<!-- wp:heading --><h2 class="wp-block-heading">Medicare and rebates</h2><!-- /wp:heading -->
<!-- wp:paragraph --><p>[Rebate wording appears here only after the practitioner confirms the exact service, eligibility and amount.] <span class="practice-draft">draft, hidden until approved</span></p><!-- /wp:paragraph -->

<!-- wp:heading --><h2 class="wp-block-heading">Do I need a referral?</h2><!-- /wp:heading -->
<!-- wp:paragraph --><p>You can book without a referral and pay the full fee. [If rebates are offered: what a referral is, who provides it and what to bring.] <span class="practice-draft">draft</span></p><!-- /wp:paragraph -->

<!-- wp:heading --><h2 class="wp-block-heading">Paying</h2><!-- /wp:heading -->
<!-- wp:paragraph --><p>[Payment is taken by card at the end of each session through the booking system.] <span class="practice-draft">confirm</span></p><!-- /wp:paragraph -->

<!-- wp:heading {"anchor":"cancellations"} --><h2 class="wp-block-heading" id="cancellations">Cancelling or changing an appointment</h2><!-- /wp:heading -->
<!-- wp:paragraph --><p>Give at least [x] hours\' notice and there\'s no fee. With less notice, [the cancellation fee] applies. Life happens, so get in touch if something unexpected comes up. <span class="practice-draft">terms to confirm</span></p><!-- /wp:paragraph -->

<!-- wp:heading --><h2 class="wp-block-heading">Your first appointment</h2><!-- /wp:heading -->
<!-- wp:list --><ul class="wp-block-list"><!-- wp:list-item --><li>It takes [50] minutes by secure video. You\'ll need a private space and a phone, tablet or computer.</li><!-- /wp:list-item --><!-- wp:list-item --><li>You\'ll talk about what\'s brought you here, at a pace that suits you. You don\'t have to share anything you\'re not ready to.</li><!-- /wp:list-item --><!-- wp:list-item --><li>Towards the end, you\'ll decide together whether to keep going and how often.</li><!-- /wp:list-item --></ul><!-- /wp:list -->

' . practice_ref( 'booking-action' ) . '

' . practice_pattern( 'urgent-help-banner' );

$fees     = practice_page( 'fees', 'Fees and first appointment', $fees_content );
$meet     = practice_page( 'meet', 'Meet [Name]', practice_pattern( 'practitioner-intro' ) . practice_stub( 'Full profile: qualifications, approach, client groups.' ) );
$services = practice_page( 'services', 'Services', practice_pattern( 'service-list' ) );
practice_page( 'service-1', '[Service 1]', practice_stub( 'Who it\'s for, what a session involves, delivery mode.' ) . practice_ref( 'fee-standard-session' ) . practice_ref( 'booking-action' ), array( 'post_parent' => $services, 'path' => 'services/service-1' ) );
practice_page( 'service-2', '[Service 2]', practice_stub( 'Who it\'s for, what a session involves, delivery mode.' ) . practice_ref( 'fee-standard-session' ) . practice_ref( 'booking-action' ), array( 'post_parent' => $services, 'path' => 'services/service-2' ) );
$how      = practice_page( 'how-sessions-work', 'How sessions work', practice_stub( 'Telehealth process and where clients can join from. Room details only once a room is confirmed.' ) );
$ref      = practice_page( 'for-referrers', 'For GPs and referrers', practice_stub( 'Verified eligibility, referral instructions, the named secure destination for referral documents.' ) );
$contact  = practice_page( 'contact', 'Contact and appointments', practice_ref( 'booking-action' ) . practice_pattern( 'contact-banner' ) . practice_pattern( 'urgent-help-banner' ) );
foreach ( array( 'privacy' => 'Privacy policy', 'complaints' => 'Feedback and complaints', 'accessibility' => 'Accessibility' ) as $s => $t ) {
	practice_page( $s, $t, practice_stub( 'Policy text, owner and review date.' ) );
}

update_option( 'show_on_front', 'page' );
update_option( 'page_on_front', $home );

// Main menu (Navigation block uses the most recent menu).
if ( ! get_posts( array( 'post_type' => 'wp_navigation', 'numberposts' => 1 ) ) ) {
	$items = array( $meet => 'Meet [Name]', $services => 'Services', $fees => 'Fees', $how => 'How sessions work', $ref => 'For GPs', $contact => 'Contact' );
	$nav   = '';
	foreach ( $items as $id => $label ) {
		$nav .= '<!-- wp:navigation-link {"label":"' . esc_attr( $label ) . '","type":"page","id":' . $id . ',"url":"' . esc_url( get_permalink( $id ) ) . '","kind":"post-type"} /-->';
	}
	wp_insert_post( wp_slash( array( 'post_type' => 'wp_navigation', 'post_status' => 'publish', 'post_title' => 'Main menu', 'post_content' => $nav ) ) );
}

echo "Pages ready.\n";
