<?php
/**
 * Title: Home hero
 * Slug: practice/hero
 * Categories: practice
 * Description: Centred headline, the shared booking action and the shared standard fee.
 */
?>
<!-- wp:group {"metadata":{"name":"Hero"},"align":"full","className":"practice-hero practice-center","style":{"spacing":{"padding":{"top":"var:preset|spacing|60","bottom":"var:preset|spacing|50"}}},"layout":{"type":"constrained","contentSize":"46rem"}} -->
<div class="wp-block-group alignfull practice-hero practice-center" style="padding-top:var(--wp--preset--spacing--60);padding-bottom:var(--wp--preset--spacing--50)">
<!-- wp:heading {"level":1} --><h1 class="wp-block-heading">You don't have to work it out alone.</h1><!-- /wp:heading -->
<!-- wp:paragraph {"className":"practice-lead"} --><p class="practice-lead">When things feel heavy, talking with a psychologist can help you make sense of it. [Name] sees adults by telehealth, anywhere in Australia. You don't need to know exactly what's wrong before you get in touch.</p><!-- /wp:paragraph -->
<?php echo practice_synced( 'booking-action' ); ?>
<?php echo practice_synced( 'fee-standard-session' ); ?>
<!-- wp:paragraph {"className":"practice-more"} --><p class="practice-more"><a href="/fees/">Fees, rebates and your first appointment</a></p><!-- /wp:paragraph -->
</div>
<!-- wp:html {"align":"wide"} -->
<div class="practice-hero-art alignwide" aria-hidden="true"><svg viewBox="0 0 1200 440" preserveAspectRatio="xMidYMax slice" focusable="false">
<defs><linearGradient id="ph-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="var(--wp--preset--color--surface)"/><stop offset="1" stop-color="var(--wp--preset--color--paper)"/></linearGradient></defs>
<rect width="1200" height="440" fill="url(#ph-sky)"/>
<circle cx="860" cy="170" r="74" fill="var(--wp--preset--color--accent)" opacity=".16"/>
<path d="M0 300 C180 230 330 250 470 280 S760 330 900 270 1120 210 1200 240 V440 H0Z" fill="var(--wp--preset--color--primary)" opacity=".14"/>
<path d="M0 340 C160 300 300 320 450 345 S720 380 880 335 1080 290 1200 310 V440 H0Z" fill="var(--wp--preset--color--primary)" opacity=".24"/>
<path d="M0 385 C200 360 360 372 520 392 S820 420 980 392 1140 370 1200 378 V440 H0Z" fill="var(--wp--preset--color--primary)" opacity=".42"/>
<path d="M0 420 C240 405 420 412 600 424 S940 438 1200 418 V440 H0Z" fill="var(--wp--preset--color--primary)" opacity=".7"/>
</svg></div>
<!-- /wp:html -->
<!-- /wp:group -->
