<?php
/**
 * Title: Common questions
 * Slug: practice/faq
 * Categories: practice
 * Description: Expandable answers to the questions people ask before booking. Practitioner approves wording.
 */
$qa = array(
	array( 'Is what I say confidential?', 'Yes. What you discuss stays private, with a few legal exceptions, such as when someone\'s safety is at serious risk or a court requires it. [Name] will explain these at your first session. <span class="practice-draft">practitioner to approve</span>' ),
	array( 'How many sessions will I need?', 'It depends on what you\'d like help with. Some people come for a few sessions, others for longer. You\'ll talk about it together, and you can stop at any time.' ),
	array( 'Is telehealth as good as seeing someone in person?', 'For many people, yes. Some also find it easier to talk from somewhere familiar. If video doesn\'t suit you, say so and [Name] can suggest options. <span class="practice-draft">confirm</span>' ),
	array( 'What if I don\'t know what to say?', 'That\'s very common. You don\'t need to prepare. [Name] will ask questions to help you get started.' ),
	array( 'Can I claim a rebate?', 'You may be able to claim a Medicare rebate with a GP referral and Mental Health Treatment Plan, or through some private health extras. <a href="/fees/#rebates">Fees and rebates</a> <span class="practice-draft">confirm</span>' ),
	array( 'Is the video platform secure?', 'Sessions use [platform], which encrypts the call. No recording is made. <span class="practice-draft">confirm platform</span>' ),
	array( 'What if I need help urgently?', 'This practice can\'t provide crisis support. If you or someone else is in danger, call 000. For support at any time, call Lifeline on 13 11 14.' ),
);
foreach ( $qa as $i => $item ) :
	?>
<!-- wp:details {"className":"practice-faq"} --><details class="wp-block-details practice-faq"><summary><?php echo $item[0]; ?></summary><!-- wp:paragraph --><p><?php echo $item[1]; ?></p><!-- /wp:paragraph --></details><!-- /wp:details -->
<?php endforeach; ?>
