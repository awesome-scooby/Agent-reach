<?php
/**
 * Title: Closing call to action
 * Slug: practice/closing-cta
 * Categories: practice
 * Description: Gentle final prompt with the shared booking action.
 */
?>
<!-- wp:group {"metadata":{"name":"Closing call to action"},"align":"full","backgroundColor":"surface","className":"practice-center","style":{"spacing":{"padding":{"top":"var:preset|spacing|60","bottom":"var:preset|spacing|60"}}},"layout":{"type":"constrained","contentSize":"36rem"}} -->
<div class="wp-block-group alignfull practice-center has-surface-background-color has-background" style="padding-top:var(--wp--preset--spacing--60);padding-bottom:var(--wp--preset--spacing--60)">
<!-- wp:heading --><h2 class="wp-block-heading">Ready when you are.</h2><!-- /wp:heading -->
<!-- wp:paragraph {"className":"practice-lead"} --><p class="practice-lead">Booking takes a few minutes. If now isn't the time, this page will be here.</p><!-- /wp:paragraph -->
<?php echo practice_synced( 'booking-action' ); ?>
</div>
<!-- /wp:group -->
