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
<!-- /wp:group -->
