# What is a bad evaluation?

So the big question you had to think about in this project was, how do you define a bad evaluation. At first I only had one clear definition which was obviously:

## Time

The evaluations should last for quite a while if the evaluator is thorough in their evaluation. But this couldn't be a static value as project like PrintF and CV do not have the same expected length of evaluation given the later has no code to talk thru. So how to do you work around that?

### Expected minimum time for projects

This would be a good way to easily distinguish short evaluations but would need a lot of manual labor to setup.

### Using average times

Later on I got the idea what you could calculate the average time used in the evaluations per project. This way you could see the ones that were shorter than average with little to no manual work required.

You would probably want to make it so you don't just check  "< average", but something like 20% shorter as on average you would match half of the evaluations to be under the average time.

**Note:** This would be very volatile value in projects/campuses with low amount of data.

### Combination

The best solution I came up with for the duration check is to combine the above ideas. In essence you would calculate the average of done evaluations and minimum eval time for each project.

So: (average_time_taken + minimum_time) / 2 \* 0.8f

This way you have an average for low data projects and you would heavily weight the average towards the time you would be happy with, while getting some change to match what the reality is.

### But...

What do you do about evaluations that didn't get the max points? Usually in the project evaluation form it is stated that if this fails you stop the evaluation. This would lead to the evaluation stopping short, unless the parties decide to continue, so the question would be if you ignore the projects that didn't get 100/125 points or got flagged for failure.

My take is that you would just simply ignore such evaluations, but there something to be said on going thru the evaluations even if it yields no points. That part depends on the parties and usually one or the other will decide to stop the evaluation there.

## Rating

The evaluated is not the only one getting rated. The evaluator will also be rated back for their work, which can be used to detect bad evaluations. Such ways are:

* One grade is really low
* The average points is low

So simple checks like "if rating.value < 2" or "if rating.average < 3" could be used to detect bad evaluations based on how the evaluated perceived it.

## Friend groups/trading

This is a social part that can also affect the quality of the evaluation. Obviously in your school or at work you will form friend groups, make connections with people and trade favours. So should these social ties affect the evaluations?

Well we wouldn't want that, but it's in reality most of the time when you do evaluations with someone you know you do not look things as thorough as with someone you don't know. That means these things could be something to consider when figuring out the quality of an evaluation.

Another part to this is trading evaluations, "I scratch your back and you will scratch mine". This is quite natural way of doing things, but consider this. You got max points from your partner, but when it's you time to evaluate them you see a small thing that would lead to errors if the memory is too low but none of the previous evaluators didn't notice it. Will you fail them for this or would you forgive them since they didn't do so thorough work on your code?

### How

The trading can be quite easy to figure out, but the hard part is the timeframe. How long between the evaluations to make the connection?

Larger social groups would be hard to figure out depending on the amount of evaluations you need per project and different paths can lead to not being able to evaluate in their main projects.

There is also the issue of amount of students and how active they are. Low amount of students per branch would lead to smaller and smaller groups going thru the projects with only that group being able to evaluate each other. Or if some students are more active at evaluating they might show up more than others which could lead to false-positives.

### Should you?

No. At the end of the day it would be almost impossible to get an accurate impression of the social ties affecting the evaluations. The trading could be something to check with things like the time taken, but other than that it would not work out.
