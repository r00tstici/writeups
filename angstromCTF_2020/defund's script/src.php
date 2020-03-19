<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width,initial-scale=1">
        <link href="https://fonts.googleapis.com/css?family=Inconsolata|Special+Elite&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="/style.css">
        <title>Defund's Crypt</title>
    </head>
    <body>
        <!-- Defund was a big fan of open source so head over to /src.php -->
        <!-- Also I have a flag in the filesystem at /flag.txt but too bad you can't read it -->
        <h1>Defund's Crypt<span class="small">o</span></h1>
        <?php
            if ($_SERVER["REQUEST_METHOD"] === "POST") {
                // I just copy pasted this from the PHP site then modified it a bit
                // I'm not gonna put myself through the hell of learning PHP to write one lousy angstrom chall
                try {
                    if (
                        !isset($_FILES['imgfile']['error']) ||
                        is_array($_FILES['imgfile']['error'])
                    ) {
                        throw new RuntimeException('The crypt rejects you.');
                    }
                    switch ($_FILES['imgfile']['error']) {
                        case UPLOAD_ERR_OK:
                            break;
                        case UPLOAD_ERR_NO_FILE:
                            throw new RuntimeException('You must leave behind a memory lest you be forgotten forever.');
                        case UPLOAD_ERR_INI_SIZE:
                        case UPLOAD_ERR_FORM_SIZE:
                            throw new RuntimeException('People can only remember so much.');
                        default:
                            throw new RuntimeException('The crypt rejects you.');
                    }
                    if ($_FILES['imgfile']['size'] > 1000000) {
                        throw new RuntimeException('People can only remember so much..');
                    }
                    $finfo = new finfo(FILEINFO_MIME_TYPE);
                    if (false === $ext = array_search(
                        $finfo->file($_FILES['imgfile']['tmp_name']),
                        array(
                            '.jpg' => 'image/jpeg',
                            '.png' => 'image/png',
                            '.bmp' => 'image/bmp',
                        ),
                        true
                    )) {
                        throw new RuntimeException("Your memory isn't picturesque enough to be remembered.");
                    }
                    if (strpos($_FILES["imgfile"]["name"], $ext) === false) {
                        throw new RuntimeException("The name of your memory doesn't seem to match its content.");
                    }
                    $bname = basename($_FILES["imgfile"]["name"]);
                    $fname = sprintf("%s%s", sha1_file($_FILES["imgfile"]["tmp_name"]), substr($bname, strpos($bname, ".")));
                    if (!move_uploaded_file(
                        $_FILES['imgfile']['tmp_name'],
                        "./memories/" . $fname
                    )) {
                        throw new RuntimeException('Your memory failed to be remembered.');
                    }
                    http_response_code(301);
                    header("Location: /memories/" . $fname);
                } catch (RuntimeException $e) {
                    echo "<p>" . $e->getMessage() . "</p>";
                }
            }
        ?>
        <img src="crypt.jpg" height="300"/>
        <form method="POST" action="/" autocomplete="off" spellcheck="false" enctype="multipart/form-data">
            <p>Leave a memory:</p>
            <input type="file" id="imgfile" name="imgfile">
            <label for="imgfile" id="imglbl">Choose an image...</label>
            <input type="submit" value="Descend">
        </form>
        <script>
            imgfile.oninput = _ => {
                imgfile.classList.add("satisfied");
                imglbl.innerText = imgfile.files[0].name;
            };
        </script>
    </body>
</html>