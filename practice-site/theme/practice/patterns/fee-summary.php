<?php
/**
 * Title: Fee summary
 * Slug: practice/fee-summary
 * Categories: practice
 * Description: Places the shared fee block. Change a fee in Patterns, not here.
 */
?>
<!-- wp:group {"metadata":{"name":"Fee summary"},"align":"full","className":"practice-center","style":{"spacing":{"padding":{"top":"var:preset|spacing|60","bottom":"var:preset|spacing|60"}}},"layout":{"type":"constrained","contentSize":"36rem"}} -->
<div class="wp-block-group alignfull practice-center" style="padding-top:var(--wp--preset--spacing--60);padding-bottom:var(--wp--preset--spacing--60)">
<!-- wp:heading --><h2 class="wp-block-heading">What it costs</h2><!-- /wp:heading -->
<?php echo practice_synced( 'fee-standard-session' ); ?>
<!-- wp:paragraph --><p>Paid at the end of each session. Cancel with at least [48] hours' notice and there's no fee. <span class="practice-draft">terms to confirm</span></p><!-- /wp:paragraph -->
<!-- wp:paragraph {"className":"practice-more"} --><p class="practice-more"><a href="/fees/">Fees, rebates and your first appointment</a></p><!-- /wp:paragraph -->
</div>
<!-- /wp:group -->
