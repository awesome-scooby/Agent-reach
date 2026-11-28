<?php
/**
 * Step 2 of 2: create pages from the theme’s patterns, the menu and the front page.
 *
 * Patterns are expanded into real blocks and saved as page content, so pages
 * belong to the database (and survive a redesign), not to the theme.
 * Placeholder data only. Safe to re-run: existing pages are left untouched.
 */

if ( ! defined( 'ABSPATH' ) ) {
	require_once '/wordpress/wp-load.php';
}

function practice_pattern( $slug, $replace = array() ) {
	$p = WP_Block_Patterns_Registry::get_instance()->get_registered( 'practice/' . $slug );
	return $p ? strtr( $p['content'], $replace ) : '';
}

function practice_page( $slug, $title, $content, $args = array() ) {
	$existing = get_page_by_path( isset( $args['path'] ) ? $args['path'] : $slug, OBJECT, 'page' );
	if ( ! $existing && isset( $args['post_status'] ) && 'publish' !== $args['post_status'] ) {
		$found    = get_posts( array( 'post_type' => 'page', 'name' => $slug, 'post_status' => 'any', 'numberposts' => 1 ) );
		$existing = $found ? $found[0] : null;
	}
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

function practice_h2( $text, $anchor = '' ) {
	$a = $anchor ? ',"anchor":"' . $anchor . '"' : '';
	$i = $anchor ? ' id="' . $anchor . '"' : '';
	return '<!-- wp:heading {' . ltrim( $a, ',' ) . '} --><h2 class="wp-block-heading"' . $i . '>' . $text . '</h2><!-- /wp:heading -->';
}

function practice_p( $html, $class = '' ) {
	$attr = $class ? ' {"className":"' . $class . '"}' : '';
	$c    = $class ? ' class="' . $class . '"' : '';
	return '<!-- wp:paragraph' . $attr . ' --><p' . $c . '>' . $html . '</p><!-- /wp:paragraph -->';
}

$draft = ' <span class="practice-draft">draft</span>';

/* Home */
$home = practice_page( 'home', 'Home', implode( "\n\n", array(
	practice_pattern( 'hero' ),
	practice_pattern( 'highlights' ),
	practice_pattern( 'is-this-for-you' ),
	practice_pattern( 'practitioner-intro' ),
	practice_pattern( 'service-list' ),
	practice_pattern( 'fee-summary' ),
	practice_pattern( 'what-happens-next' ),
	practice_pattern( 'closing-cta' ),
) ), array( 'template' => 'page-no-title' ) );

/* Fees */
$fees = practice_page( 'fees', 'Fees and first appointment', implode( "\n", array(
	practice_p( 'What a session costs, what’s covered, and what happens at your first appointment.', 'practice-lead' ),
	practice_h2( 'Session fees' ),
	practice_synced( 'fee-standard-session' ),
	practice_synced( 'fee-extended-session' ),
	practice_h2( 'Medicare rebates', 'rebates' ),
	practice_p( 'If your GP gives you a Mental Health Treatment Plan and a referral, you may be able to claim a Medicare rebate of $[rebate] per session for up to [10] sessions a calendar year. Your out-of-pocket cost would be about $[gap]. <span class="practice-draft">draft: practitioner to confirm service, eligibility and amounts before publishing</span>' ),
	practice_p( 'Private health insurance: some extras policies cover psychology. Check with your insurer. You can’t claim Medicare and private health for the same session.' . $draft ),
	practice_h2( 'Do I need a referral?', 'referral' ),
	practice_p( 'No. You can book directly and pay the full fee. You only need a GP referral if you want to claim a Medicare rebate.' . $draft ),
	practice_h2( 'Paying' ),
	practice_p( 'Payment is taken by card at the end of each session through [booking provider]. You’ll get a receipt by email.' . $draft ),
	practice_h2( 'Cancelling or changing an appointment', 'cancellations' ),
	practice_p( 'Give at least [48] hours’ notice and there’s no fee. With less notice, a fee of $[cancellation fee] applies. If something unexpected happens, get in touch.' . $draft ),
	practice_h2( 'Your first appointment' ),
	'<!-- wp:list --><ul class="wp-block-list"><!-- wp:list-item --><li>It takes [50] minutes by secure video. You’ll need a private space and a phone, tablet or computer.</li><!-- /wp:list-item --><!-- wp:list-item --><li>You’ll talk about what’s brought you here, at a pace that suits you. You don’t have to share anything you’re not ready to.</li><!-- /wp:list-item --><!-- wp:list-item --><li>Towards the end, you’ll decide together whether to keep going and how often.</li><!-- /wp:list-item --></ul><!-- /wp:list -->',
	practice_synced( 'booking-action' ),
	practice_pattern( 'urgent-help-banner' ),
) ) );

/* People and services */
$meet     = practice_page( 'meet', 'Meet [Name]', practice_pattern( 'practitioner-profile' ) . practice_synced( 'booking-action' ) );
$services = practice_page( 'services', 'Services', practice_p( 'Approved services only. Each one is delivered by telehealth.', 'practice-lead' ) . practice_pattern( 'service-list' ) );
$svc      = array(
	'anxiety-and-stress' => array( 'Anxiety and stress', 'For worry that’s hard to switch off, tension, or stress that’s affecting sleep, work or relationships.' ),
	'low-mood'           => array( 'Low mood', 'For feeling flat, unmotivated or not like yourself for a while.' ),
	'life-changes'       => array( 'Life changes and relationships', 'For a move, a loss, a break-up, a new role, or patterns that keep repeating with people.' ),
);
foreach ( $svc as $slug => $s ) {
	practice_page( $slug, $s[0], practice_pattern( 'service-detail', array( '[One sentence on who this is for.]' => $s[1] ) ), array( 'post_parent' => $services, 'path' => 'services/' . $slug ) );
}

/* Sessions, referrers, contact */
$how     = practice_page( 'how-sessions-work', 'How sessions work', practice_pattern( 'telehealth-info' ) );
$ref     = practice_page( 'for-referrers', 'For GPs and referrers', practice_pattern( 'referrer-info' ) );
$contact = practice_page( 'contact', 'Contact and appointments', practice_pattern( 'contact-page' ) . practice_pattern( 'urgent-help-banner' ) );

/* Rooms: drafts only. Nothing public until a room is confirmed. */
practice_page( 'perth-room', 'Perth room', practice_pattern( 'room', array( '[Suburb STATE Postcode]' => '[Suburb] WA [6000]', '[AWST, Perth time / AEST or AEDT, Melbourne time]' => 'AWST (Perth time)' ) ), array( 'post_status' => 'draft' ) );
practice_page( 'melbourne-room', 'Melbourne room', practice_pattern( 'room', array( '[Suburb STATE Postcode]' => '[Suburb] VIC [3000]', '[AWST, Perth time / AEST or AEDT, Melbourne time]' => 'AEST/AEDT (Melbourne time)' ) ), array( 'post_status' => 'draft' ) );

/* Policies */
$policy = practice_pattern( 'policy' );
practice_page( 'privacy', 'Privacy policy', $policy . practice_h2( 'What this policy covers' ) . practice_p( 'How [Practice legal name] collects, uses, stores and discloses personal and health information under the Privacy Act 1988 and the Australian Privacy Principles. [Template headings below; final wording to come from the practice’s actual privacy commitments.]' ) . practice_h2( 'This website' ) . practice_p( 'This website has no contact form, analytics or advertising trackers. Booking happens on [booking provider]’s site, which has its own privacy policy. [Hosting provider] keeps standard server logs for [x] days.' . $draft ) . practice_h2( 'Clinical records' ) . practice_p( '[What’s collected, why, where it’s stored, who can access it, how long it’s kept, how to request access or correction, and how to complain.]' ) );
practice_page( 'complaints', 'Feedback and complaints', $policy . practice_p( 'If you’re unhappy with any part of your care, please tell [Name] first. Email [admin@example.invalid] or call [0000 000 000]. You’ll get a response within [x] business days.' ) . practice_p( 'If you’re not satisfied, you can contact [the health complaints body for your state, e.g. HaDSCO in WA or the Health Complaints Commissioner in Victoria] or Ahpra. <span class="practice-draft">verify bodies and links for the live jurisdiction</span>' ) );
practice_page( 'accessibility', 'Accessibility', $policy . practice_p( 'This website aims to meet WCAG 2.2 level AA. It works with keyboard navigation, screen readers and text enlarged to 200%. If something doesn’t work for you, tell us at [admin@example.invalid] and we’ll fix it or give you the information another way.' ) );

update_option( 'show_on_front', 'page' );
update_option( 'page_on_front', $home );

/* Main menu (the Navigation block uses the most recent menu). */
if ( ! get_posts( array( 'post_type' => 'wp_navigation', 'numberposts' => 1 ) ) ) {
	$items = array( $meet => 'Meet [Name]', $services => 'Services', $fees => 'Fees', $how => 'How sessions work', $ref => 'For GPs', $contact => 'Contact' );
	$nav   = '';
	foreach ( $items as $id => $label ) {
		$nav .= '<!-- wp:navigation-link {"label":"' . esc_attr( $label ) . '","type":"page","id":' . $id . ',"url":"' . esc_url( get_permalink( $id ) ) . '","kind":"post-type"} /-->';
	}
	wp_insert_post( wp_slash( array( 'post_type' => 'wp_navigation', 'post_status' => 'publish', 'post_title' => 'Main menu', 'post_content' => $nav ) ) );
}

echo "Pages ready.\n";
