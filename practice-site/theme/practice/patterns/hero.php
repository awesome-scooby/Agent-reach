<?php
/**
 * Title: Home hero with booking action and fee
 * Slug: practice/hero
 * Categories: practice
 * Description: Who the practice sees, how appointments work, the shared booking action and the shared standard fee.
 */
?>
<!-- wp:group {"metadata":{"name":"Hero"},"align":"full","style":{"spacing":{"padding":{"top":"var:preset|spacing|50","bottom":"var:preset|spacing|50"}}},"layout":{"type":"constrained","contentSize":"68rem"}} -->
<div class="wp-block-group alignfull" style="padding-top:var(--wp--preset--spacing--50);padding-bottom:var(--wp--preset--spacing--50)">
<!-- wp:group {"layout":{"type":"constrained","contentSize":"44rem","justifyContent":"left"}} -->
<div class="wp-block-group">
<!-- wp:heading {"level":1} --><h1 class="wp-block-heading">When things feel heavy, you don't have to work it out alone</h1><!-- /wp:heading -->
<!-- wp:paragraph {"fontSize":"large"} --><p class="has-large-font-size">[Name] is a psychologist <span class="practice-draft">title to confirm</span> seeing [adults] by telehealth from anywhere in [Australia]. You don't need to know exactly what's wrong before you get in touch.</p><!-- /wp:paragraph -->
<?php echo practice_synced( 'booking-action' ); ?>
<?php echo practice_synced( 'fee-standard-session' ); ?>
</div>
<!-- /wp:group -->

</div>
<!-- /wp:group -->
